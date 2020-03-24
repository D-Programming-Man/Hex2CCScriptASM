#!/usr/bin/env python
import sys

# Translates a string hex number into an integer
def strToHex(numbRepDict, byte):
  hiNybble = 0
  loNybble = 0
  
  if len(byte) == 2:
    if byte[0] in numbRepDict:
      hiNybble = numbRepDict[byte[0]] * 16
    else:
      print("Symbol not supported in Hex: " + byte[0])
      sys.exit()
      
    if byte[1] in numbRepDict:
      loNybble = numbRepDict[byte[1]]
    else:
      print("Symbol not supported in Hex: " + byte[1])
      sys.exit()
      
    return hiNybble + loNybble
    
  else:
    print("Parameter pass to strToHex() is not exactly of length two: " + byte)
    sys.exit()

if __name__ == "__main__":
  inputFile = open(sys.argv[1], "r")
  out = open(sys.argv[2], "w")
  
  # Numberical symbols in hex
  numbRepDict = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4,
  "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,"A": 10, "B": 11,
  "C": 12, "D": 13, "E": 14, "F": 15}
  
  # ASM Opcodes that don't take a parameter
  noParamOps = ["0A", "00", "18", "D8",
  "58", "B8", "38", "F8",
  "78", "3A", "CA", "88",
  "1A", "E8", "C8", "4A",
  "EA", "48", "08", "DA",
  "5A", "68", "28", "FA",
  "8B", "0B", "4B", "AB",
  "2B", "2A", "40", "60",
  "6B", "DB", "AA", "A8",
  "8A", "98", "BA", "9A",
  "9B", "BB", "5B", "7B",
  "1B", "3B", "CB", "42",
  "EB", "FB", "7A", "6A"]
  
  # ASM Opcodes that take a byte parameter
  oneParamOps = ["69", "65", "72", "67",
  "75", "73", "25", "29",
  "06", "89", "24", "34",
  "90", "B0", "F0", "D0",
  "30", "10", "50", "70",
  "80", "02", "C9", "C5",
  "D1", "E0", "E4", "C0",
  "C4", "C6", "D6", "49",
  "45", "52", "E6", "A1",
  "A3", "A9", "A5", "B2",
  "B5", "B1", "B7", "A2",
  "A6", "A0", "A4", "46",
  "09", "05", "D4", "C2",
  "26", "66", "E9", "E5",
  "E2", "85", "87", "92",
  "95", "81", "91", "97",
  "86", "96", "84", "94",
  "64", "74", "14", "04",
  "A7", "E5", "7E", "E7",
  "71", "C3", "21", "01",
  "36", "07", "76", "D5",
  "77", "F7", "12", "F1",
  "51", "03"]
  
  # ASM Opcodes that take 2 byte parameters
  twoParamOps = ["69", "6D", "7D", "79",
  "29", "2D", "3D", "0E",
  "89", "2C", "3C", "82",
  "C9", "CD", "D9", "DD",
  "E0", "EC", "C0", "CC",
  "CE", "DE", "49", "4D",
  "EE", "4C", "6C", "7C",
  "DC", "20", "FC", "A9",
  "AD", "BD", "B9", "A2",
  "AE", "A0", "AC", "B4",
  "BC", "4E", "5E", "09",
  "0D", "F4", "62", "2E",
  "6E", "E9", "ED", "FE",
  "FD", "8D", "9D", "99",
  "8E", "8C", "9C", "9E",
  "1C", "0C", "1E", "59"]
  
  # ASM Opcodes that take 3 byte parameters
  threeParamOps = ["CF", "DF", "4F", "5C",
  "22", "AF", "BF", "0F",
  "1F", "EF", "FF", "8F",
  "9F"]
  
  # ASM Opcodes that has the _i and _8 suffix for the A register only
  sharedARegOps = ["69", "29", "89", "C9",
  "49", "A9","09", "E9"]
  
  # ASM Opcodes that has the _i and _8 suffix for the X/Y register only
  sharedXYRegOps = ["E0", "C0", "A2", "A0"]
  
  # All Opcodes that are not 8-bit A/X/Y register dependent
  regularOps = {"69": "ADC_i", "29": "AND_i", "89": "BIT_i", "C9": "CMP_i",
  "E0": "CPX_i", "C0": "CPY_i", "49": "EOR_i", "A9": "LDA_i", "A2": "LDX_i",
  "A0": "LDY_i", "09": "ORA_i", "E9": "SBC_i", "6D": "ADC_a", "6F": "ADC_al",
  "65": "ADC_d", "72": "ADC_di", "67": "ADC_dil", "75": "ADC_dx", "7D": "ADC_x",
  "7F": "ADC_xl", "79": "ADC_y", "73": "ADC_s", "25": "AND_d", "2D": "AND_a",
  "2F": "AND_al", "3D": "AND_x", "3F": "AND_xl", "0A": "ASL", "0E": "ASL_a",
  "06": "ASL_d", "24": "BIT_d", "34": "BIT_dx", "2C": "BIT_a", "3C": "BIT_x",
  "90": "BCC", "B0": "BCS", "F0": "BEQ", "D0": "BNE", "30": "BMI", "10": "BPL",
  "50": "BVC", "70": "BVS", "80": "BRA", "82": "BRL", "00": "BRK", "18": "CLC",
  "D8": "CLD", "58": "CLI", "B8": "CLV", "38": "SEC", "F8": "SED", "78": "SEI",
  "02": "COP", "CD": "CMP_a", "CF": "CMP_al", "C5": "CMP_d", "D9": "CMP_y",
  "DD": "CMP_x", "DF": "CMP_xl", "D1": "CMP_diy", "EC": "CPX_a", "E4": "CPX_d",
  "CC": "CPY_a", "C4": "CPY_d", "3A": "DEC", "CE": "DEC_a",  "C6": "DEC_d",
  "DE": "DEC_x", "D6": "DEC_dx", "CA": "DEX", "88": "DEY", "4D": "EOR_a",
  "4F": "EOR_al", "45": "EOR_d", "52": "EOR_di", "1A": "INC", "EE": "INC_a",
  "E6": "INC_d", "E8": "INX", "C8": "INY",  "4C": "JMP", "6C": "JMP_i",
  "7C": "JMP_ix", "5C": "JMP_l", "DC": "JMP_il", "20": "JSR", "FC": "JSR_ix",
  "22": "JSL", "A1": "LDA_dxi", "A3": "LDA_s", "AD": "LDA_a", "AF": "LDA_al",
  "A5": "LDA_d", "B2": "LDA_di", "B5": "LDA_dx", "BD": "LDA_x", "B9": "LDA_y",
  "BF": "LDA_xl", "B1": "LDA_diy", "B7": "LDA_dly", "AE": "LDX_a", "A6": "LDX_d",
  "AC": "LDY_a", "A4": "LDY_d", "B4": "LDY_dx", "BC": "LDY_x", "4A": "LSR",
  "4E": "LSR_a", "46": "LSR_d", "5E": "LSR_x", "EA": "NOP", "0D": "ORA_a",
  "0F": "ORA_al", "1F": "ORA_xl", "05": "ORA_d", "F4": "PEA", "D4": "PEI",
  "62": "PER", "48": "PHA", "08": "PHP", "DA": "PHX", "5A": "PHY", "68": "PLA",
  "28": "PLP", "FA": "PLX", "7A": "PLY", "8B": "PHB", "0B": "PHD", "4B": "PHK",
  "AB": "PLB", "2B": "PLD", "C2": "REP", "2A": "ROL", "2E": "ROL_a", "26": "ROL_d",
  "6A": "ROR", "6E": "ROR_a", "66": "ROR_d", "40": "RTI", "60": "RTS", "6B": "RTL",
  "ED": "SBC_a", "EF": "SBC_al", "E5": "SBC_d", "FD": "SBC_x", "FF": "SBC_xl",
  "E2": "SEP", "DB": "STP", "85": "STA_d", "87": "STA_dl", "92": "STA_di",
  "95": "STA_dx", "8D": "STA_a", "8F": "STA_al", "9D": "STA_x", "9F": "STA_xl",
  "99": "STA_y", "81": "STA_dxi", "91": "STA_diy", "97": "STA_dly", "8E": "STX_a",
  "86": "STX_d", "96": "STX_dy", "8C": "STY_a", "84": "STY_d", "94": "STY_dx",
  "9C": "STZ_a", "64": "STZ_d", "9E": "STZ_x", "74": "STZ_dx", "AA": "TAX",
  "A8": "TAY", "8A": "TXA", "98": "TYA", "BA": "TSX", "9A": "TXS", "BB": "TYX",
  "5B": "TCD", "7B": "TDC", "1B": "TCS", "3B": "TSC", "1C": "TRB_a", "14": "TRB_d",
  "0C": "TSB_a", "04": "TSB_d", "CB": "WAI", "42": "WDM", "EB": "XBA", "FB": "XCE",
  "9B": "TXY", "A7": "LDA_dl", "7E": "ROR_x", "E7": "SBC_dl", "71": "ADC_diy",
  "C3": "CMP_s", "21": "AND_dxi", "01": "ORA_dxi", "36": "ROL_dx", "07": "ORA_dl",
  "1E": "ASL_x", "76": "ROR_dx", "FE": "INC_x", "D5": "CMP_dx", "77": "ADC_dly",
  "F7": "SBC_dly", "59": "EOR_y", "12": "ORA_di", "03": "ORA_s", "F1": "SBC_diy",
  "51": "EOR_diy"}
  
  # All Opcodes that are 8-bit A/X/Y register dependent
  specialOps = {"69": "ADC_8", "29": "AND_8", "89": "BIT_8", "C9": "CMP_8",
  "E0": "CPX_8", "C0": "CPY_8", "49": "EOR_8", "A9": "LDA_8", "A2": "LDX_8",
  "A0": "LDY_8", "09": "ORA_8", "E9": "SBC_8"}
  
  '''
  All routines that uses the SEP opcode before returning to the routine that called it
  Some routines do a SEP/REP and then run a routine that changes the P register
    and so when it returns the P register is inconsistant and so that's why some
    of the routines in the EB ROM Explorer has weird opcodes in place
  # Key = JSR/JSL (address), Value = byte param used for SEP
  '''
  PRegSEPChangerDict = {"JSL (0xC2B66A)": "20"}
  
  PRegState = 0x00 # assume P register is 0x00 at the start
  asmOpBytes = inputFile.read().split() # Separate each byte into a list
  currentOp = 0x00  # Current ASM Opcode
  byteSizeParam = 0 # How many bytes does the current ASM Opcode require
  internalByteSize = 0 # How many bytes left do we need to decode for that Opcode
  byteParamList = [] # The concat string of the opcode to be written to a file
  pRegRoutine = "" # Some routines changes the P register when jumping back
                   # Need to keep track of routines that does this
  
  for byte in asmOpBytes:
    
    # This section is where we add the parameters to the file
    if internalByteSize > 0 and byteSizeParam >= 1:
      if currentOp == 0xC2: # REP
        PRegState = (~ strToHex(numbRepDict, byte)) & PRegState
      
      if currentOp == 0xE2: # SEP
        PRegState = strToHex(numbRepDict, byte) | PRegState
      
      byteParamList.insert(0, byte)
      internalByteSize = internalByteSize - 1
      if internalByteSize == 0:
        opParam = "".join(byteParamList)
        pRegRoutine = pRegRoutine + "(0x" + opParam + ")"
        if pRegRoutine in PRegSEPChangerDict:
          PRegState = strToHex(numbRepDict, PRegSEPChangerDict[pRegRoutine]) | PRegState
        
        # Assume most of the JSR/JSL/BRA opcodes will change P register
        # The BRA opcode is on a temporary solution, fix this when you have the addresses
          # working since we can use that to keep track of the state of the P register
        elif currentOp == 0x20 or currentOp == 0x22 or currentOp == 0x80:
          PRegState = (~ 0x30) & PRegState
        out.write("(0x" + opParam + ")\n")
        byteParamList.clear()
        pRegRoutine = ""
      continue
      
    # This section is where we determine how many params the Opcode takes
    currentOp = strToHex(numbRepDict, byte)
    special8BitOps = False
    if byte in noParamOps:
      byteSizeParam = 0
      out.write(regularOps[byte] + "\n")
      continue
      
    if byte in oneParamOps:
      byteSizeParam = 1
      internalByteSize = 1
      
    if byte in twoParamOps:
      if (byte in sharedARegOps and PRegState & 0x20 != 0) or (byte in sharedXYRegOps and PRegState & 0x10 != 0):
        byteSizeParam = 1
        internalByteSize = 1
        special8BitOps = True
      else:
        byteSizeParam = 2
        internalByteSize = 2
      
    if byte in threeParamOps:
      byteSizeParam = 3
      internalByteSize = 3
    
    if special8BitOps:
      out.write(specialOps[byte] + " ")
    else:
      out.write(regularOps[byte] + " ")
      pRegRoutine = regularOps[byte] + " "
  
  out.close()
  inputFile.close()
