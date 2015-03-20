# imap-checker

Check you imap INBOX and notifies in your beautiful desktop.

## Purpose

I am trying different mail clients in my current companies and I want to keep
up to date. Searching in different resources I decided to implement a mail 
notifier.

**imap-checker** works as a daemon polling your imap account and looking for
new emails and notifying in your desktop using `libnotify`.

## Requirements

It works in any system with `python 2.7.X` and `libnotify` installed.


## Installation

You have two options

- Using pip:

	pip install imap_checker

- Clone github repo and install dependencies in `requirements.pip` file:
	
	git clone https://github.com/VITIMan/imap-checker

## Usage

Simply copy `imap_config.example` and rename to `.imap_conf` in your home directory and change the `host`, `user` and `password` with your credentials.

Then execute:

	imap_checker

And that's it.

If you want to stop, simply use: `imap_checker --stop`.

## Improvements to consider

- Investigate about notifications in OSX systems
- Aggregate emails if you receive more than one between fetches.
