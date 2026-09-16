
# Honors SPH Fluid Sim

## Description

A 2D SPH fluid sim for a physics honors contract.

## Goals

- Real time or pre rendered fluid sim
- Interactivity of some sort such as defining liquid spawn, customizable variables, etc
- Visual impact > technical impressiveness due to audience

## Notes

### Personal Concerns

- This is a difficult and ambitious project
- I do not have the bandwidth to do a majority of work, workload needs to split evenly
- < 2 months is not a lot of time
- Reliance on AI will cripple us, all code needs to be written by you.
- This project requires a good understanding of the whole codebase, theory, and implementation
- I get ahead of myself too easily and need to be told no. I would be a bad team lead for this

### Decision point

We need to decide on a tech stack now.

#### C path

display, input, and, graphics stuff handled by raylib

##### Pros

- I personally like C
- C is very fast
- Data and CPU oriented programming is perfect for this use case
- You learn C and low level programming
- From scratch

##### Cons

- You two would need to learn:
    - C
    - data oriented programming
    - Compiled language basics
    - Cmake - I can probably set this up for us
    - Raylib
- C does not even have strings, dynamic arrays, other things you probably expect a language to have
- C does not hold you hand at all

#### Python path

We could use:
- Raylib - for real time
- MatplotLib - for pre rendered
- PyGame - I dont like PyGame but it is an option
- Taichi Lang - faster code

##### Pros

- Quicker development turnaround
- Access to OOP
- Holds your hand way more and provides more libraries and tooling

##### Cons

- slower
- More reliance on third party code
