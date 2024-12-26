// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// Replace this comment with your code.
// key = 24576

(INFLOOP)
    @24576 // set D to Mem[keyaddr]
    D=M
    @FILLSHOULD0 // if D equal to 0, jump to fill should be 0
    D;JEQ
    // fill should not be 0
    @fill // if fill = -1(and key not equal to 0), jump to infloop
    D=M+1
    @INFLOOP
    D;JEQ
    @SETFILL // else jump to setfill
    0;JMP

(FILLSHOULD0)
@fill // if fill = 0, jump to infloop
D=M
@INFLOOP
D;JEQ
@SETFILL // else jump to setfill
0;JMP

(SETFILL)
    @24576 // set D to key
    D=M
    @SETFILL0 // if D = 0, set fill 0
    D;JEQ
    @fill // else set fill to -1 (all black) and jmp to draw
    M=-1
    @DRAWINIT
    0;JMP


(SETFILL0)
    @fill // set fill to 0 and then jmp to draw
    M=0
    @DRAWINIT
    0;JMP

(DRAWINIT)
    @16384 // set location(R0) to 16384
    D=A
    @R0
    M=D

    @8191 // set counter(R1) to 8191
    D=A
    @R1
    M=D

    @fill // set R2 to fill
    D=M
    @R2
    M=D

    @DRAWLOOP // draw the screen
    0;JMP

(DRAWLOOP)
    @R2 // set D to fill
    D=M
    @R0 // set Mem[location] to D
    A=M // set new A to value of locn
    M=D // set memory at this locn to D(fill)

    @R0 // update location and counter
    M=M+1
    @R1
    M=M-1

    D=M // set D to counter
    @INFLOOP
    D;JEQ
    @DRAWLOOP
    0;JMP