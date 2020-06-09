FROM ls6uniwue/py_correction_base_image

COPY main.py main_helpers.py test_data.schema.json /data/

ENTRYPOINT ["python", "main.py"]
