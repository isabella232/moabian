#!/usr/bin/env python3

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import argparse

from controllers import (
    zero_controller,
    pid_controller,
    brain_controller,
    random_controller,
    joystick_controller,
)
from hat import Hat
from env import MoabEnv
from hat import Icon, Text
from functools import partial
from log_csv import log_decorator


CONTROLLER_INFO = {
    "pid": (pid_controller, Icon.DOT, Text.CLASSIC),
    "brain": (partial(brain_controller, port=5000), Icon.DOT, Text.BRAIN),
    "custom1": (partial(brain_controller, port=5001), Icon.DOT, Text.CUSTOM1),
    "custom2": (partial(brain_controller, port=5002), Icon.DOT, Text.CUSTOM1),
    "joystick": (joystick_controller, Icon.DOT, Text.MANUAL),
}

# Seperate each element out into its own dictionary
CONTROLLERS = {key: val[0] for key, val in CONTROLLER_INFO.items()}
ICONS = {key: val[1] for key, val in CONTROLLER_INFO.items()}
TEXTS = {key: val[2] for key, val in CONTROLLER_INFO.items()}


def main(
    controller_name,
    frequency,
    debug,
    enable_logging,
    logfile,
    use_plate_angles,
):
    icon = ICONS[controller_name]
    text = TEXTS[controller_name]

    if enable_logging:
        # Pass all arguments, if a controller doesn't need it, it will ignore it (**kwargs)
        controller = log_decorator(
            CONTROLLERS[controller_name](
                end_point=end_point,
                frequency=frequency,
            ),
            logfile=logfile,
        )
    else:
        # Pass all arguments, if a controller doesn't need it, it will ignore it (**kwargs)
        controller = CONTROLLERS[controller_name](
            frequency=frequency,
        )

    with MoabEnv(frequency, debug, use_plate_angles) as env:
        state = env.reset(icon, text)
        while True:
            action, info = controller(state)
            state = env.step(action)


if __name__ == "__main__":
    # Parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--controller",
        default="pid",
        choices=list(CONTROLLERS.keys()),
        help=f"""Select what type of action to take.
        Options are: {CONTROLLERS.keys()}
        """,
    )
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("-f", "--frequency", default=30, type=int)
    parser.add_argument("-l", "--enable_logging", action="store_true")
    parser.add_argument("-lf", "--logfile", default="/tmp/log.csv", type=str)
    parser.add_argument("-pa", "--use_plate_angles", action="store_true")
    args, _ = parser.parse_known_args()
    main(
        args.controller,
        args.frequency,
        args.debug,
        args.enable_logging,
        args.logfile,
        args.use_plate_angles,
    )
