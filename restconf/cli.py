# -*- coding: utf-8 -*-

import click

from .restconf import RestConf


CONTEXT_SETTINGS = dict(
    help_option_names=['-h'],
    obj=RestConf()
)

commands = click.Group('restconf', context_settings=CONTEXT_SETTINGS, no_args_is_help=True)

# @click.argument('hostname', nargs=1)


@commands.command()
@click.pass_context
def contexts(ctx):
    for context in ctx.obj.contexts:
        click.echo(context)


@commands.command()
@click.pass_context
def capabilities(ctx):
    for context in ctx.obj.capabilities:
        click.echo(context)


@commands.command('version')
@click.pass_context
def version(ctx):
    click.echo(ctx.obj.version)
