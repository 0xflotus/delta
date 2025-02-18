#!/usr/bin/env python3
# Copyright (C) 2017 Beijing Didi Infinity Technology and Development Co.,Ltd.
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# This file is useful for reading the contents of the ops generated by ruby.
# You can read any graph defination in pb/pbtxt format generated by ruby
# or by python and then convert it back and forth from human readable to binary format.

from absl import flags
from absl import app
from absl import logging
from pathlib import Path

import delta.compat as tf
from google.protobuf import text_format
from tensorflow.python.platform import gfile

dump_dir='pbtxt/'

def pbtxt_to_pb(filename):
  assert filename.suffix == '.pbtxt'
  with filename.open('r') as f:
    graph_def = tf.GraphDef()

    file_content = f.read()
    text_format.Merge(file_content, graph_def)

    tf.import_graph_def(graph_def, name='')
    tf.train.write_graph(graph_def, dump_dir, 'graph.pb', as_text=False)


def pb_to_pbtxt(filename):
  assert filename.suffix == '.pb'
  with filename.open('rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())

    tf.import_graph_def(graph_def, name='')
    tf.train.write_graph(graph_def, dump_dir, 'graph.pbtxt', as_text=True)
  return


def main(_):
  FLAGS = flags.FLAGS
  assert FLAGS.graph
  graph_file = Path(FLAGS.graph)

  if FLAGS.binary_in:
    pb_to_pbtxt(graph_file)
  else:
    pbtxt_to_pb(graph_file)
  logging.info(f"dump graph to {dump_dir}")

if __name__ == '__main__':
  # flags usage: https://abseil.io/docs/python/guides/flags
  logging.set_verbosity(logging.INFO)
  flags.DEFINE_string('graph', default=None, help='graph.pb file name', short_name='g')
  flags.DEFINE_bool('binary_in', default=True, help='input graph is binary or not', short_name='b')
  flags.mark_flag_as_required('graph')

  app.run(main)
