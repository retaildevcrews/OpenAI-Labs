#!/usr/bin/env python

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import json
import uuid

from flask import Flask, request

from ffmodel.core.environment_config import EnvironmentConfigs
from ffmodel.core.inference_endpoint import InferenceEndpoint
from ffmodel.data_models.inference import UserInferenceResponse
from ffmodel.utils.ffmodel_logger import FFModelLogger

# Read config
solution_config_path = EnvironmentConfigs.get_config("SOLUTION_CONFIG_PATH")
environment_config_path = EnvironmentConfigs.get_config("ENVIRONMENT_CONFIG_PATH")

# Initialize logger
logger = FFModelLogger().get_logger("app")

# Create Flask app
app = Flask(__name__)
endpoint = InferenceEndpoint(solution_config_path, environment_config_path)


@app.route("/inference", methods=["POST"])
def inference() -> str:
    request_id = uuid.uuid4()

    logger.info(f"Received request: {request_id}")
    result = endpoint.execute(request.data.decode("utf-8"))
    logger.info(f"Inference completed: {request_id}")

    response = UserInferenceResponse(
        user_nl=result.request.user_nl,
        completion=result.model_output.completions[0],
        session_id=result.request.session_id,
        sequence=result.request.sequence,
        request_id=str(request_id),
    )
    return json.dumps(response.to_dict())


app.run(host="0.0.0.0", port=8080)
