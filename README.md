# Hex2CCScriptASM
A tool used for hacking EarthBound.

As the neme implies, it interprets hex bytes into psudo assembly code that CCScript can use to compile it back into 65816 assembly hex. You will need the [asm65816.ccs](https://gist.github.com/HS39/860d79169459dc256acfbeecdb3e2281) file to see what I mean and to allow CCScript to compile it back to 65816 assembly hex. One reason why you would want to use this is to move assembly code around into the expanded area of the ROM so you can modify it how you see fit.

A website called the [Earthbound ROM Explorer](https://earthbound-rom-explorerr.herokuapp.com/) does something like this, as it translates hex to 65816 assembly, however it isn't CCScript compatable and if you want to modify a whole routine, you would have to manually write down each instruction in CCScript's psudo assembly.

This code is not used as a disassembly for the EarthBound ROM, someone is already doing that [here](https://github.com/Herringway/ebsrc). This is more of a personal project of mine to not waste time on manually copying instructions from the EarthBound ROM Explorer to CCScript.

### HOW TO RUN:
Comiple and run it like so (I use python3 to compile it, but I'm pretty sure that lower version of python would work as well):
- python3 Hex2CCScriptASM.py (input file) (output file)
  
where:
- (output file) is a text file that contains the psudo CCScript assembly code that it can interpret
  - This file can be created when compiled and ran if the output file does not exist.

- (input file) is a text file that contains only bytes represented in hex
  - You can copy bytes from the EarthBound ROM with a hex editor and then paste it into the input file
  - For example: say we have a text file called "test.txt" and it only contains these two bytes: C2 31
  - If you run this, the (output file) will contain this: REP (0x31)
  
### Future Plans:
- Most of these features are going to be replicated from the EarthBound ROM Explorer such as: addresses and labels
- Turn the output file into a CCScript block code that can be referenced as a label
- Make table addresses turn into labels so it can be easily identifiable
- BRK opcodes are appearing when there are inconsistent SEP/REP within the routine when parsing. 
  - When encountering BRK opcodes, try to add a buffer to detect them and merge with the previous opcode and update the P register
