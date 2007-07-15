# jhbuild - a build script for GNOME 1.x and 2.x
# Copyright (C) 2001-2004  James Henstridge
#
#   autobuild.py: non-interactive build that generates a report
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from optparse import make_option

from jhbuild.errors import UsageError
from jhbuild.commands.base import Command, register_command
import jhbuild.frontends

class cmd_autobuild(Command):
    '''Distributed tinderbox for jhbuild'''

    name = 'autobuild'

    def __init__(self):
        Command.__init__(self, [
            make_option('-a', '--autogen',
                        action='store_true', dest='autogen', default=False,
                        help='always run autogen.sh'),
            make_option('-c', '--clean',
                        action='store_true', dest='clean', default=False,
                        help='run make clean before make'),
            make_option('-s', '--skip', metavar='MODULES',
                        action='append', dest='skip', default=[],
                        help='treat the given modules as up to date'),
            make_option('-t', '--start-at', metavar='MODULE',
                        action='store', dest='startat', default=None,
                        help='start building at the given module'),
            make_option('-r', '--report-url',
                        action='store', dest='reporturl', default=None,
                        help='jhautobuild report URL'),
            make_option('-v', '--verbose',
                        action='store_true', dest='verbose', default=False,
                        help='verbose mode'),
            ])
    
    def run(self, config, options, args):
        config.buildscript = 'autobuild'

        config.autobuild_report_url = None
        config.verbose = False

        if options.autogen:
            config.alwaysautogen = True
        if options.clean:
            config.makeclean = True
        if options.reporturl is not None:
            config.autobuild_report_url = options.reporturl
        if options.verbose:
            config.verbose = True

        if not config.autobuild_report_url:
            raise UsageError('report url for autobuild not specified')
    
        module_set = jhbuild.moduleset.load(config)
        module_list = module_set.get_module_list(args or config.modules,
                                                 config.skip)
    
        # remove modules up to startat
        if options.startat:
            while module_list and module_list[0].name != options.startat:
                del module_list[0]
            if not module_list:
                raise FatalError('%s not in module list' % options.startat)
    
        build = jhbuild.frontends.get_buildscript(config, module_list)
        build.build()

register_command(cmd_autobuild)
