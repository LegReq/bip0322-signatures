# BIP-0322 Signatures

[BIP-0322: Generic Signed Message Format](https://github.com/bitcoin/bips/blob/master/bip-0322.mediawiki)

The aim of this repository is to demonstrate how the Bitcoin Improvement Proposal (BIP) 0322 for a generic signed message format could be used to sign Verifiable Credentials from a Bitcoin address. Ultimately, this address will be identified through a did:btcr DID. 

This repository makes use of the [buidl-python](https://github.com/buidl-bitcoin/buidl-python/) Bitcoin library developed by Jimmy Song. It also uses Jupyter Notebooks to document the approach taken when implementing the BIP 0322 specification.

## Author

- Will Abramson
- Legendary Requirements
- <a href='mailto://will@legreq.com'>will@legreq.com</a>

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
