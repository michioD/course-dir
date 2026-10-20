	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 15, 0	sdk_version 15, 5
	.globl	_handle_sigint                  ; -- Begin function handle_sigint
	.p2align	2
_handle_sigint:                         ; @handle_sigint
	.cfi_startproc
; %bb.0:
	sub	sp, sp, #32
	stp	x29, x30, [sp, #16]             ; 16-byte Folded Spill
	add	x29, sp, #16
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	stur	w0, [x29, #-4]
	adrp	x0, l_.str@PAGE
	add	x0, x0, l_.str@PAGEOFF
	bl	_printf
	adrp	x8, _server_fd@GOTPAGE
	ldr	x8, [x8, _server_fd@GOTPAGEOFF]
	ldr	w0, [x8]
	bl	_close
	mov	w0, #0                          ; =0x0
	bl	_exit
	.cfi_endproc
                                        ; -- End function
	.globl	_start_server                   ; -- Begin function start_server
	.p2align	2
_start_server:                          ; @start_server
	.cfi_startproc
; %bb.0:
	sub	sp, sp, #64
	stp	x29, x30, [sp, #48]             ; 16-byte Folded Spill
	add	x29, sp, #48
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	adrp	x8, ___stack_chk_guard@GOTPAGE
	ldr	x8, [x8, ___stack_chk_guard@GOTPAGEOFF]
	ldr	x8, [x8]
	stur	x8, [x29, #-8]
	str	w0, [sp, #20]
	mov	w1, #1                          ; =0x1
	str	w1, [sp, #16]
	mov	w0, #2                          ; =0x2
	mov	w2, #0                          ; =0x0
	bl	_socket
	adrp	x8, _server_fd@GOTPAGE
	ldr	x8, [x8, _server_fd@GOTPAGEOFF]
	str	w0, [x8]
	cbnz	w0, LBB1_2
	b	LBB1_1
LBB1_1:
	adrp	x0, l_.str.1@PAGE
	add	x0, x0, l_.str.1@PAGEOFF
	bl	_perror
	mov	w0, #1                          ; =0x1
	bl	_exit
LBB1_2:
	adrp	x8, _server_fd@GOTPAGE
	ldr	x8, [x8, _server_fd@GOTPAGEOFF]
	ldr	w0, [x8]
	mov	w1, #65535                      ; =0xffff
	mov	w4, #4                          ; =0x4
	mov	x2, x4
	add	x3, sp, #16
	bl	_setsockopt
	cbz	w0, LBB1_4
	b	LBB1_3
LBB1_3:
	adrp	x0, l_.str.2@PAGE
	add	x0, x0, l_.str.2@PAGEOFF
	bl	_perror
	mov	w0, #1                          ; =0x1
	bl	_exit
LBB1_4:
	mov	w8, #2                          ; =0x2
	strb	w8, [sp, #25]
	str	wzr, [sp, #28]
	b	LBB1_5
LBB1_5:
	ldr	w8, [sp, #20]
	and	w0, w8, #0xffff
	bl	__OSSwapInt16
	str	w0, [sp, #12]                   ; 4-byte Folded Spill
	b	LBB1_6
LBB1_6:
	ldr	w8, [sp, #12]                   ; 4-byte Folded Reload
	add	x1, sp, #24
	strh	w8, [sp, #26]
	adrp	x8, _server_fd@GOTPAGE
	ldr	x8, [x8, _server_fd@GOTPAGEOFF]
	ldr	w0, [x8]
	mov	w2, #16                         ; =0x10
	bl	_bind
	tbz	w0, #31, LBB1_8
	b	LBB1_7
LBB1_7:
	adrp	x0, l_.str.3@PAGE
	add	x0, x0, l_.str.3@PAGEOFF
	bl	_perror
	mov	w0, #1                          ; =0x1
	bl	_exit
LBB1_8:
	adrp	x8, _server_fd@GOTPAGE
	ldr	x8, [x8, _server_fd@GOTPAGEOFF]
	ldr	w0, [x8]
	mov	w1, #3                          ; =0x3
	bl	_listen
	tbz	w0, #31, LBB1_10
	b	LBB1_9
LBB1_9:
	adrp	x0, l_.str.4@PAGE
	add	x0, x0, l_.str.4@PAGEOFF
	bl	_perror
	mov	w0, #1                          ; =0x1
	bl	_exit
LBB1_10:
	ldr	w8, [sp, #20]
                                        ; kill: def $x8 killed $w8
	mov	x9, sp
	str	x8, [x9]
	adrp	x0, l_.str.5@PAGE
	add	x0, x0, l_.str.5@PAGEOFF
	bl	_printf
	adrp	x8, _server_fd@GOTPAGE
	ldr	x8, [x8, _server_fd@GOTPAGEOFF]
	ldr	w8, [x8]
	str	w8, [sp, #8]                    ; 4-byte Folded Spill
	ldur	x9, [x29, #-8]
	adrp	x8, ___stack_chk_guard@GOTPAGE
	ldr	x8, [x8, ___stack_chk_guard@GOTPAGEOFF]
	ldr	x8, [x8]
	subs	x8, x8, x9
	b.eq	LBB1_12
	b	LBB1_11
LBB1_11:
	bl	___stack_chk_fail
LBB1_12:
	ldr	w0, [sp, #8]                    ; 4-byte Folded Reload
	ldp	x29, x30, [sp, #48]             ; 16-byte Folded Reload
	add	sp, sp, #64
	ret
	.cfi_endproc
                                        ; -- End function
	.p2align	2                               ; -- Begin function _OSSwapInt16
__OSSwapInt16:                          ; @_OSSwapInt16
	.cfi_startproc
; %bb.0:
	sub	sp, sp, #16
	.cfi_def_cfa_offset 16
	strh	w0, [sp, #14]
	ldrh	w9, [sp, #14]
	ldrh	w8, [sp, #14]
	asr	w8, w8, #8
	orr	w8, w8, w9, lsl #8
	and	w0, w8, #0xffff
	add	sp, sp, #16
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_dashboard_loop                 ; -- Begin function dashboard_loop
	.p2align	2
_dashboard_loop:                        ; @dashboard_loop
	.cfi_startproc
; %bb.0:
	sub	sp, sp, #32
	stp	x29, x30, [sp, #16]             ; 16-byte Folded Spill
	add	x29, sp, #16
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	str	x0, [sp, #8]
	ldr	x8, [sp, #8]
	str	x8, [sp]
	b	LBB3_1
LBB3_1:                                 ; =>This Inner Loop Header: Depth=1
	ldr	x0, [sp]
	bl	_print_dashboard
	mov	w0, #1                          ; =0x1
	bl	_sleep
	b	LBB3_1
	.cfi_endproc
                                        ; -- End function
	.globl	_print_dashboard                ; -- Begin function print_dashboard
	.p2align	2
_print_dashboard:                       ; @print_dashboard
	.cfi_startproc
; %bb.0:
	sub	sp, sp, #80
	stp	x29, x30, [sp, #64]             ; 16-byte Folded Spill
	add	x29, sp, #64
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	stur	x0, [x29, #-8]
	adrp	x0, l_.str.6@PAGE
	add	x0, x0, l_.str.6@PAGEOFF
	bl	_printf
	adrp	x0, l_.str.7@PAGE
	add	x0, x0, l_.str.7@PAGEOFF
	bl	_printf
	adrp	x0, l_.str.8@PAGE
	add	x0, x0, l_.str.8@PAGEOFF
	str	x0, [sp, #32]                   ; 8-byte Folded Spill
	bl	_printf
	mov	x9, sp
	adrp	x8, l_.str.10@PAGE
	add	x8, x8, l_.str.10@PAGEOFF
	str	x8, [x9]
	adrp	x8, l_.str.11@PAGE
	add	x8, x8, l_.str.11@PAGEOFF
	str	x8, [x9, #8]
	adrp	x8, l_.str.12@PAGE
	add	x8, x8, l_.str.12@PAGEOFF
	str	x8, [x9, #16]
	adrp	x8, l_.str.13@PAGE
	add	x8, x8, l_.str.13@PAGEOFF
	str	x8, [x9, #24]
	adrp	x0, l_.str.9@PAGE
	add	x0, x0, l_.str.9@PAGEOFF
	bl	_printf
	ldr	x0, [sp, #32]                   ; 8-byte Folded Reload
	bl	_printf
	stur	wzr, [x29, #-12]
	b	LBB4_1
LBB4_1:                                 ; =>This Inner Loop Header: Depth=1
	ldur	w8, [x29, #-12]
	ldur	x9, [x29, #-8]
	ldr	w9, [x9, #248]
	subs	w8, w8, w9
	b.ge	LBB4_4
	b	LBB4_2
LBB4_2:                                 ;   in Loop: Header=BB4_1 Depth=1
	ldur	x8, [x29, #-8]
	add	x8, x8, #8
	ldursw	x9, [x29, #-12]
	mov	x10, #24                        ; =0x18
	mul	x9, x9, x10
	add	x8, x8, x9
	stur	x8, [x29, #-24]
	ldur	x8, [x29, #-24]
	ldr	x12, [x8]
	ldur	x8, [x29, #-24]
	ldrb	w10, [x8, #12]
	adrp	x9, l_.str.16@PAGE
	add	x9, x9, l_.str.16@PAGEOFF
	adrp	x8, l_.str.15@PAGE
	add	x8, x8, l_.str.15@PAGEOFF
	and	w10, w10, #0x1
	ands	w10, w10, #0x1
	csel	x11, x8, x9, ne
	ldur	x8, [x29, #-24]
	ldr	w8, [x8, #16]
	mov	x10, x8
	ldur	x8, [x29, #-24]
	ldr	w8, [x8, #20]
                                        ; kill: def $x8 killed $w8
	mov	x9, sp
	str	x12, [x9]
	str	x11, [x9, #8]
	str	x10, [x9, #16]
	str	x8, [x9, #24]
	adrp	x0, l_.str.14@PAGE
	add	x0, x0, l_.str.14@PAGEOFF
	bl	_printf
	b	LBB4_3
LBB4_3:                                 ;   in Loop: Header=BB4_1 Depth=1
	ldur	w8, [x29, #-12]
	add	w8, w8, #1
	stur	w8, [x29, #-12]
	b	LBB4_1
LBB4_4:
	adrp	x0, l_.str.8@PAGE
	add	x0, x0, l_.str.8@PAGEOFF
	bl	_printf
	ldur	x8, [x29, #-8]
	ldr	w8, [x8]
                                        ; kill: def $x8 killed $w8
	mov	x9, sp
	str	x8, [x9]
	adrp	x0, l_.str.17@PAGE
	add	x0, x0, l_.str.17@PAGEOFF
	bl	_printf
	ldp	x29, x30, [sp, #64]             ; 16-byte Folded Reload
	add	sp, sp, #80
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_main                           ; -- Begin function main
	.p2align	2
_main:                                  ; @main
	.cfi_startproc
; %bb.0:
	sub	sp, sp, #384
	stp	x28, x27, [sp, #352]            ; 16-byte Folded Spill
	stp	x29, x30, [sp, #368]            ; 16-byte Folded Spill
	add	x29, sp, #368
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	.cfi_offset w27, -24
	.cfi_offset w28, -32
	stur	wzr, [x29, #-20]
	stur	w0, [x29, #-24]
	stur	x1, [x29, #-32]
	mov	w0, #2                          ; =0x2
	adrp	x1, _handle_sigint@PAGE
	add	x1, x1, _handle_sigint@PAGEOFF
	bl	_signal
	add	x0, sp, #80
	str	x0, [sp, #8]                    ; 8-byte Folded Spill
	mov	x2, #256                        ; =0x100
	adrp	x1, l___const.main.config@PAGE
	add	x1, x1, l___const.main.config@PAGEOFF
	bl	_memcpy
	ldr	x3, [sp, #8]                    ; 8-byte Folded Reload
	add	x0, sp, #72
	mov	x1, #0                          ; =0x0
	str	x1, [sp]                        ; 8-byte Folded Spill
	adrp	x2, _health_check_loop@GOTPAGE
	ldr	x2, [x2, _health_check_loop@GOTPAGEOFF]
	bl	_pthread_create
	ldr	x1, [sp]                        ; 8-byte Folded Reload
	ldr	x3, [sp, #8]                    ; 8-byte Folded Reload
	add	x0, sp, #64
	adrp	x2, _dashboard_loop@PAGE
	add	x2, x2, _dashboard_loop@PAGEOFF
	bl	_pthread_create
	ldr	w0, [sp, #80]
	bl	_start_server
	str	w0, [sp, #60]
	b	LBB5_1
LBB5_1:                                 ; =>This Inner Loop Header: Depth=1
	add	x2, sp, #40
	mov	w8, #16                         ; =0x10
	str	w8, [sp, #40]
	ldr	w0, [sp, #60]
	add	x1, sp, #44
	bl	_accept
	str	w0, [sp, #36]
	ldr	w8, [sp, #36]
	tbz	w8, #31, LBB5_3
	b	LBB5_2
LBB5_2:                                 ;   in Loop: Header=BB5_1 Depth=1
	adrp	x0, l_.str.19@PAGE
	add	x0, x0, l_.str.19@PAGEOFF
	bl	_perror
	b	LBB5_1
LBB5_3:                                 ;   in Loop: Header=BB5_1 Depth=1
	mov	x0, #16                         ; =0x10
	bl	_malloc
	str	x0, [sp, #24]
	ldr	w8, [sp, #36]
	ldr	x9, [sp, #24]
	str	w8, [x9]
	ldr	x9, [sp, #24]
	add	x8, sp, #80
	str	x8, [x9, #8]
	ldr	x3, [sp, #24]
	add	x0, sp, #16
	mov	x1, #0                          ; =0x0
	adrp	x2, _handle_client@GOTPAGE
	ldr	x2, [x2, _handle_client@GOTPAGEOFF]
	bl	_pthread_create
	cbz	w0, LBB5_5
	b	LBB5_4
LBB5_4:                                 ;   in Loop: Header=BB5_1 Depth=1
	adrp	x0, l_.str.20@PAGE
	add	x0, x0, l_.str.20@PAGEOFF
	bl	_perror
	ldr	w0, [sp, #36]
	bl	_close
	ldr	x0, [sp, #24]
	bl	_free
	b	LBB5_6
LBB5_5:                                 ;   in Loop: Header=BB5_1 Depth=1
	ldr	x0, [sp, #16]
	bl	_pthread_detach
	b	LBB5_6
LBB5_6:                                 ;   in Loop: Header=BB5_1 Depth=1
	b	LBB5_1
	.cfi_endproc
                                        ; -- End function
	.section	__TEXT,__cstring,cstring_literals
l_.str:                                 ; @.str
	.asciz	"\nShutting down server...\n"

	.comm	_server_fd,4,2                  ; @server_fd
l_.str.1:                               ; @.str.1
	.asciz	"socket failed"

l_.str.2:                               ; @.str.2
	.asciz	"setsockopt"

l_.str.3:                               ; @.str.3
	.asciz	"bind failed"

l_.str.4:                               ; @.str.4
	.asciz	"listen"

l_.str.5:                               ; @.str.5
	.asciz	"Load balancer listening on port %d\n"

l_.str.6:                               ; @.str.6
	.asciz	"\033[H\033[J"

l_.str.7:                               ; @.str.7
	.asciz	"C-LOAD-BALANCER Dashboard\n"

l_.str.8:                               ; @.str.8
	.asciz	"----------------------------------------------------------------------\n"

l_.str.9:                               ; @.str.9
	.asciz	"%-20s %-10s %-10s %-10s\n"

l_.str.10:                              ; @.str.10
	.asciz	"Backend"

l_.str.11:                              ; @.str.11
	.asciz	"Status"

l_.str.12:                              ; @.str.12
	.asciz	"Active"

l_.str.13:                              ; @.str.13
	.asciz	"Total"

l_.str.14:                              ; @.str.14
	.asciz	"%-20s %-10s %-10d %-10d\n"

l_.str.15:                              ; @.str.15
	.asciz	"UP"

l_.str.16:                              ; @.str.16
	.asciz	"DOWN"

l_.str.17:                              ; @.str.17
	.asciz	"Listening on port: %d\n"

l_.str.18:                              ; @.str.18
	.asciz	"127.0.0.1"

	.section	__DATA,__const
	.p2align	3, 0x0                          ; @__const.main.config
l___const.main.config:
	.long	8080                            ; 0x1f90
	.space	4
	.quad	l_.str.18
	.long	8081                            ; 0x1f91
	.byte	1                               ; 0x1
	.space	3
	.long	0                               ; 0x0
	.long	0                               ; 0x0
	.quad	l_.str.18
	.long	8082                            ; 0x1f92
	.byte	1                               ; 0x1
	.space	3
	.long	0                               ; 0x0
	.long	0                               ; 0x0
	.space	192
	.long	2                               ; 0x2
	.space	4

	.section	__TEXT,__cstring,cstring_literals
l_.str.19:                              ; @.str.19
	.asciz	"accept"

l_.str.20:                              ; @.str.20
	.asciz	"Failed to create client thread"

.subsections_via_symbols
