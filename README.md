# Korrekturtool für Unittests

TODO...

## Erforderliche Dateien im Container

* `/data/results.json` (`rw`):

  Leere Datei, in der die Resultate geschrieben werden
  
* `/data/test_conf.json` (`ro`):

  Datei mit Testkonfiguration, Schema nach `test_conf.schema.json`

* `/data/<ex_name>/<ex_name>_test.py`:

  Datei mit Unittests
  
* `/data/<ex_name>/<ex_name>_<num>.py`:

  Jeweils eine Datei für jeden Testfall in `test_conf.json`