from buidl.tx import Tx, TxIn, TxOut
from buidl.script import Script,P2WPKHScriptPubKey
from buidl.helper import big_endian_to_int, base64_decode, base64_encode, str_to_bytes

from buidl.script import address_to_script_pubkey
from buidl.hash import tagged_hash
from buidl.witness import Witness

from buidl.ecc import PrivateKey

import io
from enum import Enum


class MessageSignatureFormat(Enum):
    LEGACY = 0
    SIMPLE = 1
    FULL = 2
    

def hash_bip322message(msg: bytes):

    # Byte array of message hash
    # The tag defined in BIP0322 that should be used
    tag = b"BIP0322-signed-message"

    return tagged_hash(tag,msg)



def create_to_spend_tx(address, message):
    # Not a valid Tx hash. Will never be spendable on any BTC network.
    prevout_hash = bytes.fromhex('0000000000000000000000000000000000000000000000000000000000000000')
    # prevout.n
    prevout_index = big_endian_to_int(bytes.fromhex('FFFFFFFF'))
    
    sequence = 0

    b_msg = str_to_bytes(message)
    message_hash = hash_bip322message(b_msg)

    # Note BIP322 to_spend scriptSig commands = [0, 32, message_hash]
    # PUSH32 is implied and added by the size of the message added to the stack
    commands = [0, message_hash]
    script_sig = Script(commands)
    # Create Tx Input
    tx_in = TxIn(prevout_hash,prevout_index,script_sig,sequence)
    
    # Value of tx output
    value = 0

    # Convert address to a ScriptPubKey
    # Will throw runtime error if unable to convert address to script_pubkey
    script_pubkey = address_to_script_pubkey(address)
        
    print("Is taproot", script_pubkey.is_p2tr())

    tx_out = TxOut(value,script_pubkey)
    
    # create transaction
    version=0
    tx_inputs = [tx_in]
    tx_outputs = [tx_out]
    locktime=0
    network="mainnet"

    # Could be false, but using a segwit address. I think this is the "Simple Signature" in BIP-0322
    segwit=True

    return Tx(version,tx_inputs,tx_outputs,locktime,network,segwit)


def create_to_sign_tx(to_spend_tx_hash, sig_bytes=None):
    to_sign = None
    if (sig_bytes and is_full_signature(sig_bytes)):
        
        sig_stream = io.BytesIO(sig_bytes)
        to_sign = Tx.parse(sig_stream)
        
        if (len(to_sign.tx_ins) > 1):
            
            raise NotImplemented("Not yet implemented proof of funds yet")
        elif (len(to_sign.tx_ins) == 0):
            raise ValueError("No transaction input")
        elif (to_sign.tx_ins[0].prev_tx != to_spend_tx_hash):
            print("prev_tx",to_sign.tx_ins[0].prev_tx)
            print("to_spend_hash",to_spend_tx_hash)
            raise ValueError("The to_sign transaction input's prevtx id does not equal the calculated to_spend transaction id")
        elif (len(to_sign.tx_outs) != 1):
            raise ValueError("to_sign does not have a single TxOutput")
        elif (to_sign.tx_outs[0].amount != 0):
            raise ValueError("Value is Non 0", to_sign.tx_outs[0].amount)
        elif(to_sign.tx_outs[0].script_pubkey.commands != [106]):
            raise ValueError("ScriptPubKey incorrect", to_sign.tx_outs[0].script_pubkey)
        else:
            return to_sign
            
    else:
        # signature is either None or an encoded witness stack
        
        # Identifies the index of the output from the virtual to_spend tx to be "spent"
        prevout_index = 0

        sequence = 0

        # TxInput identifies the output from to_spend
        tx_input = TxIn(to_spend_tx_hash,prevout_index,script_sig=None,sequence=sequence)
        

    
        value = 0
        # OP Code 106 for OP_RETURN
        commands = [106]
        scriptPubKey = Script(commands)

        tx_output = TxOut(value,scriptPubKey)
        
        version=0
        tx_inputs = [tx_input]
        tx_outputs = [tx_output]
        locktime=0
        network="mainnet"
        # Could be false, but using a segwit address. I think this is the "Simple Signature" in BIP-0322
        segwit=True
    
        # create unsigned to_sign transaction

        to_sign_tx = Tx(version,tx_inputs,tx_outputs,locktime,network,segwit)
        
        if sig_bytes:
            try:
                stream = io.BytesIO(sig_bytes)
                witness = Witness.parse(stream)
                # Set the witness on the to_sign tx input
                to_sign_tx.tx_ins[0].witness = witness
            except:
                # TODO: Fall back to legacy ...
                print("Signature is niether an encoded witness or full transaction. Fall back to legacy")
                return None
                
        return to_sign_tx

# Test is sig_bytes can be decoded to a transaction
# TODO: Is there a betterw way to test than this?
def is_full_signature(sig_bytes):
    try:
        sig_stream = io.BytesIO(sig_bytes)

        Tx.parse(sig_stream)
    # TODO: more specific exception handling
    except:
        print("Signature is not full")
        return False
    return True
        

def sign_message(format: MessageSignatureFormat, private_key: PrivateKey, address: str, message: str):
    
    if (format != MessageSignatureFormat.LEGACY):
        return sign_message_bip322(format,private_key,address,message)


    script_pubkey = address_to_script_pubkey(address)
    
    if (not script_pubkey.is_p2pkh):
        raise ValueError("Address must be p2pkh for LEGACY signatures")
        
    b_msg = str_to_bytes(message)
    signature = private_key.sign_message(b_msg)
    
    return base64_encode(signature.der())    
    
    

def sign_message_bip322(format: MessageSignatureFormat, private_key: PrivateKey, address: str, message: str):
    
    assert(format != MessageSignatureFormat.LEGACY)
        
    # TODO: how can we check the private key "controls" the provided address
    
    to_spend = create_to_spend_tx(address, message)
    to_sign = create_to_sign_tx(to_spend.hash(), None)
    
    to_sign.tx_ins[0]._script_pubkey = to_spend.tx_outs[0].script_pubkey
    to_sign.tx_ins[0]._value = to_spend.tx_outs[0].amount
    
    sig_ok = to_sign.sign_input(0, private_key)
    
    
    # Force the format to FULL, if this turned out to be a legacy format (p2pkh) signature
    if (len(to_sign.tx_ins[0].script_sig.commands) > 0 or len(to_sign.tx_ins[0].witness.items) == 0):
        format = MessageSignatureFormat.FULL

    print(to_sign)
    print("txIn tap script", to_sign.tx_ins[0].tap_script)
    print("txIn witness", to_sign.tx_ins[0].witness)
    print(sig_ok)
    combined_script = to_sign.tx_ins[0].script_sig + to_sign.tx_ins[0].script_pubkey("mainnet")
    print("Combined Script", combined_script)
    if (not sig_ok):
        raise RuntimeError("Unable to sign message")
    
    if (format ==  MessageSignatureFormat.SIMPLE):
            return base64_encode(to_sign.serialize_witness())

    else:
        return base64_encode(to_sign.serialize())

def verify_message(address: str, signature: str, message: str):

    sig_bytes = base64_decode(signature)
        
    to_spend = create_to_spend_tx(address, message)
    
    
    to_sign = create_to_sign_tx(to_spend.hash(), sig_bytes)
    
    if to_sign == None:
        # try LEGACY
        # Check address is a p2pkh
        # Recover Secp256 point from signature?
        # Verify signature
        raise NotImplementedError("TODO")
    
    to_sign.tx_ins[0]._script_pubkey = to_spend.tx_outs[0].script_pubkey
    to_sign.tx_ins[0]._value = to_spend.tx_outs[0].amount
    return to_sign.verify_input(0)
    