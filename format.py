#!/usr/bin/env python

import argparse
import os

from jinja2 import Template
import yaml

def get_templates(format):
  with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'formats', '%s.yml' % format)) as io:
    yml = yaml.safe_load(io)
    return Template(yml['template']), Template(yml['filename'])

def render(spec, format):
  tpl, fnameTpl = get_templates(format)
  return tpl.render(**spec), fnameTpl.render(**spec)

def main(specs, format, crlf, outdir):
  for spec in specs:
    with open(spec, 'r') as input:
      contents, filename = render(yaml.safe_load(input), format)
      with open(os.path.join(outdir, filename), 'w+', newline='\r\n' if crlf else '\n') as output:
        output.write(contents)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('specs', metavar='SPEC', nargs='+')
  parser.add_argument('--format', default='cht', choices=['cht', 'pnach'])
  parser.add_argument('--crlf', default=False, action='store_true')
  parser.add_argument('--outdir', default='out')
  args = parser.parse_args()

  main(args.specs, args.format, args.crlf, args.outdir)
