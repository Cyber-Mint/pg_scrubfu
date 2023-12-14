import click

@click.command()
@click.help_option('-h', '--help')
@click.version_option('0.1.0', '-v', '--version', message='%(prog)s v%(version)s')
@click.argument('infile', type=click.File('r'), default='-', required=False)
@click.argument('outfile', type=click.File('w'), default='-', required=False)
@click.option('--log', default='-', help='Optional LOGFILE, defaults to standard out.')
@click.option('--log_level', default='error', type=click.Choice(['error', 'info', 'debug']), help='Used with [--log=LOGFILE].')
@click.option('--ref_fk', is_flag=True, help='Flag: also scrubfu related foreign key data.')



def cli(log, ref_fk, log_level, infile, outfile):
	"""
	pg_scrubfu v0.1.0, Copyright(c) 2020, Cyber-Mint (Pty) Ltd
	
	   Distributed under the MIT license.
	
	pg_crubfu is a script that makes creating usable development data
	from production data a predictable, audit-able and repeatable process.
	The script works by scrubbing and /or obsfucating table column data
	based on script-tags in SQL comments stored in the postgres database.\n
	[INFILE] is the input file obtained by a pg_dump.\n	
	[OUTFILE] is the scrubfu'ed file, ready to be imported with pg_import.\n
	For further details see: https://github.com/Cyber-Mint/pg_scrubfu\n
	
	"""
	pass
	#click.echo('Scrubfu will write to %s' % outfile, file=outfile)
	#click.echo(infile)
	#if !ref_fk:
	#	raise click.BadParameter('Dude - Applying to related fk data is always preferred', param_hint=['--ref_fk'])

if __name__ == '__main__':
	cli()

