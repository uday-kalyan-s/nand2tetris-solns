// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

//// Replace this comment with your code.

@R2 // set R2 to 0
M=0

@R1 // set counter to R1+1 to acct for 0 edge case
D=M 
@counter
M=D+1

(LOOP)
    @R0 // R2 = R2 + R0
    D=M
    @R2
    M=D+M

    @counter
    M=M-1
    D=M
    @LOOP
    D;JGT

@R0
D=M
@R2
M=M-D

(INFLOOP)
@INFLOOP
0;JMP