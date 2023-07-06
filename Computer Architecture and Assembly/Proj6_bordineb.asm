TITLE Portfolio Project     (Prog6_bordineb.asm)

; Author: Brendan Bordine
; Last Modified: 
; OSU email address: bordineb@oregonstate.edu
; Course number/section: CS-271-400
; Project Number: 6               Due Date: 08/13/2021
; Description: This program takes 10 signed integers as inputs from the user
;	and manually translates the ASCII to integers and outputs the integers' sum
;	and average as ASCII.

INCLUDE Irvine32.inc

ARRAYSIZE EQU 10

getString MACRO bufferaddr, buffertyp, bufsize, prompt
; Gets an input string to return the input in buffer
	push	edx
	push	ecx
	push	eax

	mov		edx, prompt
	call	WriteString

	mov		edx, bufferaddr
	mov		ecx, buffertyp
	call	ReadString

	mov		[bufsize], eax

	pop		eax
	pop		ecx
	pop		edx

ENDM


displayString MACRO outputValue
; Takes a value and outputs it as a string to the console
	push	edx
	mov		edx, outputValue
	call	WriteString
	pop		edx

ENDM

.data

user_input		DWORD	ARRAYSIZE DUP(0)
sum_input		DWORD	?
buffer			BYTE	64 DUP(0)
input_size		BYTE	?
program_title	BYTE	\
"Assignment 6: String Primitives and Macros", 13, 10, 0
program_author	BYTE	"Written by: Brendan Bordine", 13, 10, 0
program_instruction1	BYTE	"Please provide 10 signed decimal integers.", 0
program_instruction2	BYTE	\
"Each number needs to be small enough to fit inside a 32 bit register.", 0
program_instruction3	BYTE	\
"After you have finished inputting the raw numbers I will display a list", 0
program_instruction4	BYTE	"of the integers, their sum, and their average value.",0
program_prompt	BYTE	"Please enter an signed number: ", 0
program_interr	BYTE	\
"ERROR: You did not enter a signed number or your number was too big.",13,10,0
program_tryagain	BYTE	"Please try again: ", 0
program_display1	BYTE	"You entered the following numbers:", 13, 10, 0
program_display2	BYTE	"The sum of these numbers is: ", 0
program_display3	BYTE	"The rounded average is: ", 0
program_goodbye	BYTE	"Thanks for playing!", 13, 10, 0
program_space	BYTE	"  ", 0


.code
main PROC

	mov		edx, OFFSET program_title
	call	WriteString

	mov		edx, OFFSET program_author
	call	WriteString

	call	CrLf

	push	OFFSET program_instruction4
	push	OFFSET program_instruction3
	push	OFFSET program_instruction2
	push	OFFSET program_instruction1
	call	Instruction

	call	CrLf

	push	OFFSET program_tryagain
	push	LENGTHOF buffer
	push	OFFSET input_size
	push	OFFSET buffer
	push	OFFSET program_interr
	push	OFFSET program_prompt
	push	SIZEOF user_input
	push	OFFSET user_input
	call	ArrayFill

	call	CrLf

	mov		edx, OFFSET program_display1
	call	WriteString

	push	LENGTHOF buffer
	push	OFFSET program_space
	push	OFFSET buffer
	push	ARRAYSIZE
	push	OFFSET user_input
	call	ArrayOut

	call	CrLf
	call	CrLf

	mov		edx, OFFSET program_display2
	call	WriteString

	push	LENGTHOF buffer
	push	OFFSET buffer
	push	OFFSET sum_input
	push	ARRAYSIZE
	push	OFFSET user_input
	call	Sum

	call	CrLf

	mov		edx, OFFSET program_display3
	call	WriteString

	push	LENGTHOF buffer
	push	OFFSET buffer
	push	sum_input
	push	ARRAYSIZE
	call	Avg

	call	CrLf

	mov		edx, OFFSET program_goodbye
	call	WriteString

	exit	; exit to operating system
main ENDP


Instruction PROC
; Give instructions to the user program and detail the functions.
	push	ebp
	mov		ebp, esp

	mov		ecx, 4
	mov		esi, ebp
	add		esi, 8

Loop1:	mov		edx, [esi]
	call	WriteString
	call	CrLf

	add		esi, 4
	
	loop	Loop1

	pop		ebp
	ret		16
Instruction ENDP


ReadValue PROC
LOCAL	currentValue:DWORD, signFlag:BYTE
; Read and validate the user input using getString macro.

	mov		signFlag, 0
	mov		currentValue, 0
	mov		esi, [ebp + 8]
	mov		ebx, [ebp + 16]

Input:
	; Get the user input
	getString esi, [ebp + 12], [ebp + 24], ebx

	; Setup to process input
	xor		eax, eax
	xor		ebx, ebx
	mov		ax, 1

	; Prepare loop
	cld
	mov		ebx, 1
	mov		ecx, [ebp + 24]
	sub		ecx, 1
	cmp		ecx, 0
	jz		Loop1

	; The input should be a certain length
	cmp		ecx, 11
	jg		Invalid

	mov		ebx, 10

Mult:		; Set multiplier
	mul		ebx
	loop	Mult

	mov		ebx, eax
	mov		ecx, [ebp + 24]

	xor		eax, eax

Loop1:		; LOOP: For each char in the string
			; load the last value
	lodsb

	; End at the null
	cmp		al, 0
	je		Finish

	; if there is a plus sign valid but need go to next
	cmp		al, 43
	je		Loop1
	
	; Check for a negative sign
	cmp		al, 45
	jne		Cont

	mov		signFlag, 1

	; Two's Complement
	xor		eax, 0
	add		eax, 1
	jmp		Loop1

Cont:		; Check to make sure the input is an integer value
	cmp		al, 48
	jl		Invalid

	cmp		al, 57
	jg		Invalid

	; Store value
	sub		al, 48
	mul		ebx
	mov		edx, currentValue
	add		eax, edx
	mov		currentValue, eax

	cmp		signFlag, 1
	je		isNegative
	
	cmp		eax, 7FFFFFFFh
	jo		Invalid
	jle		Value

isNegative:
	cmp		eax, 80000000h
	jo		Invalid

Value:
	xor		edx, edx

	; Divide by 10
	mov		eax, ebx
	mov		ebx, 10
	cdq
	div		ebx
	mov		ebx, eax
	jmp		Finish

Invalid:		; Invalid input
	mov		edx, [ebp + 20]
	call	WriteString

	mov		ebx, [ebp + 28]
	mov		currentValue, 0
	mov		signFlag, 0

	jmp		Input

Finish:
	; loop until current input is transfered
	dec		ecx
	cmp		ecx, 0
	jg		Loop1

	mov		eax, currentValue

	ret		24
ReadValue ENDP


ArrayFill PROC
; Fill the user input array via ReadValue.

	push	ebp
	mov		ebp, esp

	mov		esi, [ebp + 24]
	mov		edi, [ebp + 8]

Input:
	; Check if finished
	mov		eax, [ebp + 12]
	add		eax, [ebp + 8]
	cmp		edi, eax
	jge		Finish

	push	[ebp + 36]
	push	[ebp + 28]
	push	[ebp + 20]
	push	[ebp + 16]
	push	[ebp + 32]
	push	esi
	call	ReadValue

	mov		[edi], eax

Next:		; Go to next number in array
	mov		esi, [ebp + 24]
	add		edi, 4
	jmp		Input

Finish:
	; Clean the buffer and input_size
	mov		edi, [ebp + 24]
	mov		ecx, [ebp + 32]

Loop2:	mov		BYTE PTR [edi], 0
	add		edi, 1

	loop	Loop2

	mov		esi, [ebp + 28]
	mov		esi, 0

	pop		ebp
	ret		32
ArrayFill ENDP

WriteValue PROC
LOCAL	currentValue:DWORD
; Subprocedure to convert signed integers to strings.

	; Prepare to display
	mov		eax, [ebp + 8]
	mov		currentValue, eax
	mov		edi, [ebp + 12]

	cld

	; Check if negative
	test	eax, 0
	jns		isPos

	; Two's Complement
	xor		eax, eax
	add		eax, 1

	; Add minus sign
	mov		ebx, eax
	xor		eax, eax
	mov		al, 45
	stosb

	mov		eax, ebx
	mov		currentValue, eax

isPos:		; A positive number
	; Setup
	mov		ebx, 10
	cmp		eax, 10
	jle		OneDigit

Loop2:			; Divide by 10
	cdq
	div		ebx
	cmp		eax, 10
	jl		Accum

	; If quotient is larger than 10
	; go in multiples of 10 until < 10
	mov		eax, ebx
	mov		ebx, 10
	mul		ebx
	mov		ebx, eax
	mov		eax, currentValue
	jmp		Loop2

Accum:		; Store ASCII value
	add		al, 48
	stosb

	; move remainder
	mov		eax, edx
	mov		currentValue, eax

	; If more than 10 then continue
	cmp		eax, 10
	jge		isPos

	; Only one's place is left
OneDigit:
	add		al, 48
	stosb

	; Display the value
	mov		edi, [ebp + 12]
	displayString edi

	ret		8
WriteValue ENDP

ArrayOut PROC
; Output the user input using the displayString macro.

	push	ebp
	mov		ebp, esp

	; Setup
	mov		ecx, [ebp + 12]
	mov		esi, [ebp + 8]
	
Loop1:			; LOOP: for all numbers in the array
	mov		edi, [ebp + 16]
	mov		eax, [esi]
	
	push	edi
	push	eax
	call	WriteValue

	mov		edx, [ebp + 20]
	call	WriteString

	mov		edx, [ebp + 24]
	add		edx, edi

Clear:
	mov		BYTE PTR [edi], 0
	add		edi, 1

	cmp		edi, edx
	jl		Clear

	; Got to next value in array
	add		esi, 4
	loop	Loop1

	pop		ebp
	ret		20
ArrayOut ENDP

Sum PROC
; Add the numbers and display the sum.

	push	ebp
	mov		ebp, esp

	xor		eax, eax

	mov		ecx, [ebp + 12]
	mov		esi, [ebp + 8]
	mov		edi, [ebp + 16]

Loop1:			; Add all the numbers
	mov		ebx, [esi]
	add		eax, ebx
	add		esi, 4
	loop	Loop1

	; Store value for later
	mov		[edi], eax

	; Recall buffer
	mov		edi, [ebp + 20]

	; Write sum
	push	edi
	push	eax
	call	WriteValue

	; Clean the buffer
	mov		edx, [ebp + 24]
	add		edx, edi

Clear:
	mov		BYTE PTR [edi], 0
	add		edi, 1

	cmp		edi, edx
	jl		Clear

	pop		ebp
	ret		20
Sum ENDP

Avg PROC
; Display sum.

	push	ebp
	mov		ebp, esp
	xor		eax, eax

	; Take the sum and array length, then divide for the average
	mov		ebx, [ebp + 8]
	mov		eax, [ebp + 12]

	cdq
	div		ebx

	; Recall buffer
	mov		edi, [ebp + 16]

	push	edi
	push	eax
	call	WriteValue
	
	; Clean the buffer
	mov		edx, [ebp + 20]
	add		edx, edi

Clear:
	mov		BYTE PTR [edi], 0
	add		edi, 1

	cmp		edi, edx
	jl		Clear

	pop		ebp
	ret		16
Avg ENDP

END main
© 2021 GitHub, Inc.