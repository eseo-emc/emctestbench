#include <FTCJTAG.h>
                    
#define MAX_FREQ_DEVICE_CLOCK_DIVISOR 29 // default is 29 equivalent to 1MHz

#define PIN_LOW false
#define PIN_HIGH true
#define PIN_OUT true
#define PIN_IN false
#define NUM_DEVICE_CMD_CONTROL_BITS 8  
#define NUM_DEVICE_CMD_CONTROL_BYTES 1

#define NUM_DEVICE_CMD_DATA_BITS 8 
#define NUM_DEVICE_CMD_DATA_BYTES 1

#define MAX_READ_DATA_BYTES_BUFFER_SIZE 65536
#define MAX_WRITE_DATA_BYTES_BUFFER_SIZE 65536

#define IR_LENGTH_BITS_ABT8245		8
#define IR_LENGTH_BYTES_ABT8245		1
#define BSR_LENGTH_BITS_ABT8245		36
#define BSR_LENGTH_BYTES_ABT8245	5
#define INTEST_EXTEST_ABT8245		0x03
#define SAMPLE_PRELOAD_ABT8245		0x82
#define	DATA_REG			0
#define INSTRUCTION_REG			1

FTC_STATUS FTC_Status = FTC_SUCCESS;
FTC_HANDLE ftHandleA, ftHandleB = 0;
BYTE timerValue = 0;
DWORD dwNumHiSpeedDevices = 0;
DWORD dwHiSpeedDeviceIndex = 0;
DWORD dwLocationID = 0;
DWORD dwHiSpeedDeviceType = 0;
DWORD dwClockFrequencyHz = 0;
float freq_JTAG_flt;
FTC_INPUT_OUTPUT_PINS LowInputOutputPins;
FTC_LOW_HIGH_PINS LowPinsInputData;
FTH_INPUT_OUTPUT_PINS HighInputOutputPinsA, HighInputOutputPinsB;
FTH_LOW_HIGH_PINS HighPinsInputData;
WriteControlByteBuffer WriteControlBuffer;
WriteDataByteBuffer WriteDataBuffer;
ReadDataByteBuffer ReadDataBuffer;
DWORD dwNumDataBytesReturned = 0;
BYTE InputState_8245, PortAState_8245, PortBState_8245;


void UpdateInputs_8245(void) {
	InputState_8245 = 0;
	for (i=0; i<8; i++)
		if (bit_values[i] == 1)
			InputState_8245 |= (1<<i);
	if (InputMode_8245 == PINS) { // set FT2232H AC bus
	 	HighInputOutputPinsA.bPin1LowHighState = bit_values[0];
	 	HighInputOutputPinsA.bPin2LowHighState = bit_values[1];
	 	HighInputOutputPinsA.bPin3LowHighState = bit_values[2];
	 	HighInputOutputPinsA.bPin4LowHighState = bit_values[3];
	 	HighInputOutputPinsA.bPin5LowHighState = bit_values[4];
	 	HighInputOutputPinsA.bPin6LowHighState = bit_values[5];
	 	HighInputOutputPinsA.bPin7LowHighState = bit_values[6];
	 	HighInputOutputPinsA.bPin8LowHighState = bit_values[7];
		FTC_Status = JTAG_SetHiSpeedDeviceGPIOs(ftHandleA, false, &LowInputOutputPins, true, &HighInputOutputPinsA);
	}
	// otherwise output BSCs will be written when reading output pins (no latches in '245)
}


void EvaluateImmunity_ABT8245(void) {
	int i, errors, bit_values[8];
	DWORD bytes_read;
	
	errors = 0;
	if (InputMode_8245 == PINS) {
		// Read port A input BSCs (A_I)
		WriteDataBuffer[0] = SAMPLE_PRELOAD_8245;
		for(i=0; i < 100; i++) {
			FTC_Status = JTAG_Write(ftHandleA, INSTRUCTION_REG, IR_LENGTH_BITS_ABT8245, &WriteDataBuffer,
				IR_LENGTH_BYTES_ABT8245, RUN_TEST_IDLE_STATE);
			FTC_Status = JTAG_Read(ftHandleA, DATA_REG, BSR_LENGTH_BITS_ABT8245, &ReadDataBuffer,
				&bytes_read, TEST_LOGIC_STATE);
			PortAState_8245 = ReadDataBuffer[1]; 		// A_I 
			if (PortAState_8245 != InputState_8245)
				errors++;
		}
	}
	else
		for(i=0; i < 100; i++) {
			// Set port B output BSCs (B_O) and port A input BSCs (A_I)
			WriteDataBuffer[0] = INTEST_EXTEST_8245;
			FTC_Status = JTAG_Write(ftHandleA, INSTRUCTION_REG, IR_LENGTH_BITS_ABT8245, &WriteDataBuffer,
				IR_LENGTH_BYTES_ABT8245, RUN_TEST_IDLE_STATE);
			WriteDataBuffer[4] = 10;			// OEB = 1, OEA = 0, DIR = 1, _OE = 0
			WriteDataBuffer[3] = 0;				// B_I
			WriteDataBuffer[2] = InputState_8245;		// B_O
			WriteDataBuffer[1] = InputState_8245; 		// A_I
			WriteDataBuffer[0] = 0;				// A_O
			FTC_Status = JTAG_Write(ftHandleA, DATA_REG, BSR_LENGTH_BITS_ABT8245, &WriteDataBuffer,
				BSR_LENGTH_BYTES_ABT8245, RUN_TEST_IDLE_STATE);
			// Read FT2232H BC bus
			FTC_Status = JTAG_GetHiSpeedDeviceGPIOs(ftHandleB, false, &LowPinsInputData, true, &HighPinsInputData);
			PortBState_8245 = HighPinsInputData.bPin1LowHighState;
			PortBState_8245 |= (HighPinsInputData.bPin2LowHighState << 1);
			PortBState_8245 |= (HighPinsInputData.bPin3LowHighState << 2);
			PortBState_8245 |= (HighPinsInputData.bPin4LowHighState << 3);
			PortBState_8245 |= (HighPinsInputData.bPin5LowHighState << 4);
			PortBState_8245 |= (HighPinsInputData.bPin6LowHighState << 5);
			PortBState_8245 |= (HighPinsInputData.bPin7LowHighState << 6);
			PortBState_8245 |= (HighPinsInputData.bPin8LowHighState << 7);
			if (PortBState_8245 != InputState_8245)
				errors++;
		}
}

int Open_JTAG(void)
{
	int freq_div;
	
	FTC_Status = JTAG_GetNumHiSpeedDevices(&dwNumHiSpeedDevices);
	if ((FTC_Status == FTC_SUCCESS) && (dwNumHiSpeedDevices > 0))
	    	do {
			FTC_Status = JTAG_GetHiSpeedDeviceNameLocIDChannel(dwHiSpeedDeviceIndex, szDeviceName, 100, &dwLocationID,
				szChannel, 5, &dwHiSpeedDeviceType);
			dwHiSpeedDeviceIndex = dwHiSpeedDeviceIndex + 1; 
		}
		while ((FTC_Status == FTC_SUCCESS) && (dwHiSpeedDeviceIndex < dwNumHiSpeedDevices) && (strcmp(szChannel, "A") != 0));
	else 
		return -1;
	}
	// Canal A
	FTC_Status = JTAG_OpenHiSpeedDevice(szDeviceName, dwLocationID, szChannel, &ftHandleA);
	FTC_Status = JTAG_InitDevice(ftHandleA, MAX_FREQ_DEVICE_CLOCK_DIVISOR);
	FTC_Status = JTAG_TurnOffDivideByFiveClockingHiSpeedDevice(ftHandleA);
	freq_div = (int) (30.0/freq_JTAG_flt)-1;
	FTC_Status = JTAG_SetClock(ftHandleA, freq_div, &dwClockFrequencyHz);

	LowInputOutputPins.bPin1InputOutputState = PIN_OUT;
	LowInputOutputPins.bPin1LowHighState = PIN_LOW;		  // OE
	LowInputOutputPins.bPin2InputOutputState = PIN_OUT;
	LowInputOutputPins.bPin2LowHighState = PIN_HIGH;	  // A to B
	LowInputOutputPins.bPin3InputOutputState = PIN_OUT;
	LowInputOutputPins.bPin3LowHighState = PIN_LOW;
	LowInputOutputPins.bPin4InputOutputState = PIN_OUT;   
	LowInputOutputPins.bPin4LowHighState = PIN_LOW;      
	HighInputOutputPinsA.bPin1InputOutputState = PIN_OUT;
	HighInputOutputPinsA.bPin1LowHighState = PIN_LOW;
	HighInputOutputPinsA.bPin2InputOutputState = PIN_OUT;
	HighInputOutputPinsA.bPin2LowHighState = PIN_LOW;
	HighInputOutputPinsA.bPin3InputOutputState = PIN_OUT;
	HighInputOutputPinsA.bPin3LowHighState = PIN_LOW;
	HighInputOutputPinsA.bPin4InputOutputState = PIN_OUT;   
	HighInputOutputPinsA.bPin4LowHighState = PIN_LOW;      
	HighInputOutputPinsA.bPin5InputOutputState = PIN_OUT;
	HighInputOutputPinsA.bPin5LowHighState = PIN_LOW;
	HighInputOutputPinsA.bPin6InputOutputState = PIN_OUT;
	HighInputOutputPinsA.bPin6LowHighState = PIN_LOW;
	HighInputOutputPinsA.bPin7InputOutputState = PIN_OUT;
	HighInputOutputPinsA.bPin7LowHighState = PIN_LOW;
	HighInputOutputPinsA.bPin8InputOutputState = PIN_OUT;
	HighInputOutputPinsA.bPin8LowHighState = PIN_LOW;
	FTC_Status = JTAG_SetHiSpeedDeviceGPIOs(ftHandleA, true, &LowInputOutputPins, true, &HighInputOutputPinsA);

	// Canal B
	do {
		FTC_Status = JTAG_GetHiSpeedDeviceNameLocIDChannel(dwHiSpeedDeviceIndex, szDeviceName, 100, &dwLocationID,
			szChannel, 5, &dwHiSpeedDeviceType);
		dwHiSpeedDeviceIndex = dwHiSpeedDeviceIndex + 1;
	}
	while ((FTC_Status == FTC_SUCCESS) && (dwHiSpeedDeviceIndex < dwNumHiSpeedDevices) && (strcmp(szChannel, "B") != 0));
	FTC_Status = JTAG_OpenHiSpeedDevice(szDeviceName, dwLocationID, szChannel, &ftHandleB);
	FTC_Status = JTAG_InitDevice(ftHandleB, MAX_FREQ_DEVICE_CLOCK_DIVISOR);
	FTC_Status = JTAG_SetClock(ftHandleB, freq_div, &dwClockFrequencyHz);
	FTC_Status = JTAG_TurnOffDivideByFiveClockingHiSpeedDevice(ftHandleB);
	HighInputOutputPinsB.bPin1InputOutputState = PIN_IN;
	HighInputOutputPinsB.bPin1LowHighState = PIN_LOW;
	HighInputOutputPinsB.bPin2InputOutputState = PIN_IN;
	HighInputOutputPinsB.bPin2LowHighState = PIN_LOW;
	HighInputOutputPinsB.bPin3InputOutputState = PIN_IN;
	HighInputOutputPinsB.bPin3LowHighState = PIN_LOW;
	HighInputOutputPinsB.bPin4InputOutputState = PIN_IN;   
	HighInputOutputPinsB.bPin4LowHighState = PIN_LOW;      
	HighInputOutputPinsB.bPin5InputOutputState = PIN_IN;
	HighInputOutputPinsB.bPin5LowHighState = PIN_LOW;
	HighInputOutputPinsB.bPin6InputOutputState = PIN_IN;
	HighInputOutputPinsB.bPin6LowHighState = PIN_LOW;
	HighInputOutputPinsB.bPin7InputOutputState = PIN_IN;
	HighInputOutputPinsB.bPin7LowHighState = PIN_LOW;
	HighInputOutputPinsB.bPin8InputOutputState = PIN_IN;
	HighInputOutputPinsB.bPin8LowHighState = PIN_LOW;
	FTC_Status = JTAG_SetHiSpeedDeviceGPIOs(ftHandleB, false, &LowInputOutputPins, true, &HighInputOutputPinsB);

	return 0;
}

void Close_JTAG(void)
{
	if (ftHandleA != NULL)
		FTC_Status = JTAG_Close(ftHandleA);
	if (ftHandleB != NULL)
		FTC_Status = JTAG_Close(ftHandleB);
}

