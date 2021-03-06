---
title: OpEn on Raspberry Pi
author: Pantelis Sopasakis
authorURL: http://twitter.com/isToxic
authorImageURL: https://pbs.twimg.com/profile_images/1062281000171003904/KkolV9Eg_400x400.jpg
---

Here we give an example of building a parametric optimizer in MATLAB, which will run on a **Raspberry Pi**. The parametric optimizer will listen for requests on a **UDP socket**. We will then establish a connection to the optimizer, remotely, and consume the service.

![Raspberry Pi](/optimization-engine/img/rpi.jpeg)

<!--truncate-->

**NOTE:** Please, read the documentation of the [MATLAB interface](../../../../docs/matlab-interface) and the [UDP communication protocol](../../../../docs/udp-sockets) first.

In MATLAB, we run the following script:

```matlab
nu = 6;                            % number of decision variables
np = 2;                            % number of parameters 

u = casadi.SX.sym('u', nu);        % decision variables
p = casadi.SX.sym('p', np);        % parameters

phi = rosenbrock(u, p);            % cost function phi(u; p) (Rosenbrock)

constraints = OpEnConstraints.make_ball_at_origin(1.0);

build_config = open_build_config();
build_config.target = 'rpi';
build_config.build_mode = 'release';
build_config.udp_interface.bind_address = '0.0.0.0';
build_config.udp_interface.port = 3498;

open_generate_code(build_config, constraints, u, p, phi);
```

Note that we have specified that the target hardware is a raspberry pi, `rpi` (equivalently `arm-unknown-linux-gnueabihf`), the bind address is `0.0.0.0` (so that the service will bind on all valid IP addresses) and the port is `3498`. We have also set the `build_mode` to `release` for maximum performance.

After we execute the script, the code generator will have created a new project at

```text
build/autogenerated_optimizer/
```

We then copy the binary file from 

```text
build/autogenerated_optimizer/target/arm-unknown-linux-gnueabihf/release
```

onto our Raspberry Pi and execute it.

Then, on our PC (assuming we run on Linux), we run:

```bash
netcat -u {ip_address_of_raspberry} 3498
```

where `{ip_address_of_raspberry}` is the IP address (or domain name) of our Raspberry. This will start a console, where we can send data to the PI. For example, we write

```json
{"parameter":[50, 100]}
```

and press Enter, to receive:


```json
{
	"p" : [50.0, 100.0],
	"u" : [1.2597243950, 1.3938323941, 1.6995734606, 2.6752011118, 7.0289056698, 49.3661825375],
	"n" : 88,
	"f" : -5.243242641581731,
	"dt" : "1.207756ms"
}
```

So, **what do you think**? Let us know by providing some feedback (you can reach us live [**here**](../../../2019/03/06/talk-to-us)). 

If you like **OpEn**, please give it [**a star on github**](https://github.com/alphaville/optimization-engine). 

If you find a bug, please create [**an issue on on github**](https://github.com/alphaville/optimization-engine/issues/new).