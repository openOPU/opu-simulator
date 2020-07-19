# OPU Simulator

This the reference simulator for the OPU ISA. 

Currently, it only supports the following configuration:
- `ITYPE` = int8
- `KTYPE` = int8
- `BTYPE` = int16
- `OTYPE` = int16

## Requirements

- python3 with numpy


## Interface

The simulator can be launched using 
```
python sim.py
```

The simulator supports three commands: `write`, `read`, and `run`.

### Write command
```
write $addr $value
```
This command writes the byte value `$value` into memory at address `$addr`.   

`$value` and `$addr` must be indicated in decimal form.  
`$value` must be in the interval [0, 255]. `$addr` must be in the interval [0, 2^32 - 1].

### Read command
```
read $addr
```
This command reads the byte value stored at address `$addr` and writes it to the standard output.

`$addr` must be indicated in decimal form.
`$addr` must be in the interval [0, 2^32 - 1].

### Run command
```
run $filename
```
This commands simulates the execution of the program contained in the binary file `$filename`.

