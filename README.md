# BIP-0322 Signatures

[BIP-0322: Generic Signed Message Format](https://github.com/bitcoin/bips/blob/master/bip-0322.mediawiki)

The aim of this repository is to demonstrate how the Bitcoin Improvement Proposal (BIP) 0322 for a generic signed message format could be used to sign Verifiable Credentials from a Bitcoin address. Ultimately, this address will be identified through a did:btcr DID. 

This repository makes use of the [buidl-python](https://github.com/buidl-bitcoin/buidl-python/) Bitcoin library developed by Jimmy Song. It also uses Jupyter Notebooks to document the approach taken when implementing the BIP 0322 specification.

Currently implemented in repo:

- BIP 322 Walkthrough [Signing](./BIP0322_signing.ipynb), [Verification](./BIP0322_verification.ipynb)
- BIP 322 Buidl Python [API](./BIP322_interface.ipynb) and [library](./src/message.py). This has been submitted as a P.R. to [buidl-python](https://github.com/buidl-bitcoin/buidl-python/pull/140)
- [BIP 322 p2sh multisig](./p2sh_multisig_bip322/)
- [BIP 322 p2wsh multisig](./p2wsh_multisig_bip322/)
- WIP [BIP322 Signatures for Verifiable Credentials](./vc/)
- WIP [BIP322 p2tr signature](./experiments/taproot_bip322.ipynb)

## Author

- Will Abramson
- Legendary Requirements
- <a href='mailto://will@legreq.com'>will@legreq.com</a>

## Acknowledgements

This work was funded by Ryan Grant, [Digital Contract Design](https://contract.design/). Thanks also go to Joe Andrieu, Kalle Alm, Pieter Wuille and Jimmy Song for engaging with and supporting various aspects of this work.

# Using the Repo

## Note: These instructions are for a linux machine

## Pre-requisites

* Python v3.8
* Pip


## Install Dependencies

1. Create a virtual environment
```
python -m venv venv
```

2. Activate the virtual environment
```
source venv/bin/activate
```

3. Install python packages
```
pip install -r requirements.txt
```

## Run Notebooks

4. Launch the jupyter server
```
jupyter notebook
```

5. Run through the notebooks

shift + enter runs a cell
