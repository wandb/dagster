import os
from unittest.mock import patch

import pytest
import wandb.sdk as wandb_sdk
from dagster_wandb import wandb_resource

from dagster import DagsterResourceFunctionError, build_op_context, op


def test_wandb_resource_invalid_key():
    with pytest.raises(DagsterResourceFunctionError):
        build_op_context(resources={"wandb": wandb_resource.configured({"api_key": "dummy"})})


@patch("wandb.login")
@patch("wandb.config")
@patch("wandb.init")
@patch("wandb.finish")
@patch("wandb.log")
@patch("wandb.save")
@patch("wandb.agent")
@patch("wandb.sweep")
@patch("wandb.Artifact")
def test_resource_methods(artifact, sweep, agent, save, log, finish, init, config, login):
    @op(required_resource_keys={"wandb"})
    def test_dummy_op(context):
        assert context.resources.wandb

        context.resources.wandb.config({"epochs": 4, "batch_size": 32})
        config.assert_called_with({"epochs": 4, "batch_size": 32})

        context.resources.wandb.init()
        init.assert_called_once()

        context.resources.wandb.finish(exit_code=123)
        finish.assert_called_with(exit_code=123)

        context.resources.wandb.log({"accuracy": 0.9, "epoch": 5})
        log.assert_called_with({"accuracy": 0.9, "epoch": 5})

        context.resources.wandb.save(policy="now")
        save.assert_called_with(policy="now")

        def sweep_fn():
            pass

        context.resources.wandb.sweep({"name": "my-awesome-sweep"})
        sweep.assert_called_with({"name": "my-awesome-sweep"})

        context.resources.wandb.agent(1, function=sweep_fn)
        agent.assert_called_with(1, function=sweep_fn)

        context.resources.wandb.Artifact("mnist", type="dataset")
        artifact.assert_called_with("mnist", type="dataset")

        return True

    test_ctx = build_op_context(
        resources={"wandb": wandb_resource.configured({"api_key": "mock_key"})}
    )
    login.assert_called_with(key="mock_key")
    assert test_dummy_op(test_ctx)
