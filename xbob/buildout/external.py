#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.dos.anjos@gmail.com>
# Tue 17 Apr 19:16:46 2012 

"""A simple recipe to let buildout add external eggs (as egg-links).
"""

import os
import fnmatch
import logging
import zc.buildout

from .tools import *

class Recipe(object):
  """Sets up links to egg installations depending on user configuration
  """

  def __init__(self, buildout, name, options):

    self.name = name
    self.options = options
    self.logger = logging.getLogger(self.name)
    self.buildout = buildout
    
    self.logger.debug("Initializing '%s'" % self.name)

    self.eggdirs = parse_list(options.get('egg-directories', ''))

    remove = []
    for k in self.eggdirs:
      d = os.path.abspath(k)
      if not os.path.exists(d):
        self.logger.warn("Ignoring unknown egg directory '%s'" % d)
        remove.append(k)

    self.eggdirs = [os.path.abspath(k) for k in self.eggdirs if k not in remove]

    self.logger.debug("Found %d valid egg directory(ies)" % len(self.eggdirs))

    self.only_glob = options.get('include-glob', '*.egg')
      
    self.buildout_eggdir = buildout['buildout'].get('eggs-directory')

    self.recurse = buildout['buildout'].get('recurse', '1') in ('1', 'true')
    
    self.strict_version = buildout['buildout'].get('strict-version', '1') in ('1', 'true')

  def install(self):

    def create_egg_link(distro):
      '''Generates the egg-link file'''

      basename = os.path.splitext(os.path.basename(distro.location))[0]
      link = os.path.join(self.buildout_eggdir, basename) + '.egg-link'
      f = open(link, 'wt')
      f.write(distro.location + '\n')
      f.close()
      self.options.created(link)

    eggs = []
    if self.recurse:
      for path in self.eggdirs:
        for (dirpath, dirnames, filenames) in os.walk(path):
          names = fnmatch.filter(dirnames, self.only_glob) + \
              fnmatch.filter(filenames, self.only_glob)
          eggs += [os.path.join(dirpath, k) for k in names]
    else:
      for path in self.eggdirs:
        names = fnmatch.filter(os.listdir(path), self.only_glob)
        eggs += [os.path.join(path, k) for k in names]

    # resolve versions and package names (only consider strict versions)
    from pkg_resources import find_distributions
    from distutils.version import StrictVersion
    distros = [d[0] for d in [list(find_distributions(k)) for k in eggs]]
    if self.strict_version:
      distros = [d for d in distros if StrictVersion.version_re.match(d.version)]
      self.logger.info("Found %d version-strict egg(s)" % len(distros))
    else:
      self.logger.debug("Found %d non-version-strict egg(s)" % len(distros))

    for k in distros:
      self.logger.info("Linking external egg %s" % k.location)
      create_egg_link(k)

    return self.options.created()

  update = install
