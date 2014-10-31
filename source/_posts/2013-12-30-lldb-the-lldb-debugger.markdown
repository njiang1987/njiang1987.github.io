---
layout: post
title: '[lldb] The LLDB Debugger'
categories:
- 未分类
tags: []
published: true
comments: true
---
<p><h1>GDB TO LLDB COMMAND MAP</h1>
<div /></p>

<p>Below is a table of GDB commands with the LLDB counterparts. The built in GDB-compatibility aliases in LLDB are also listed. The full lldb command names are often long, but any unique short form can be used. Instead of "<b>breakpoint set</b>", "<b>br se</b>" is also acceptable.</p>

<p>
<div></div>
<h1>EXECUTION COMMANDS</h1>
<div /></p>

<p>&nbsp;
<table width="620" cellspacing="0">
<tbody>
<tr>
<td width="50%">GDB</td>
<td width="50%">LLDB</td>
</tr>
<tr>
<td colspan="2">Launch a process no arguments.</td>
</tr>
<tr>
<td><b>(gdb)</b> run
<b>(gdb)</b> r</td>
<td><b>(lldb)</b> process launch
<b>(lldb)</b> run
<b>(lldb)</b> r</td>
</tr>
<tr>
<td colspan="2">Launch a process with arguments <code>&lt;args&gt;</code>.</td>
</tr>
<tr>
<td><b>(gdb)</b> run &lt;args&gt;
<b>(gdb)</b> r &lt;args&gt;</td>
<td><b>(lldb)</b> process launch -- &lt;args&gt;
<b>(lldb)</b> r &lt;args&gt;</td>
</tr>
<tr>
<td colspan="2">Launch a process for with arguments <b><code>a.out 1 2 3</code></b> without having to supply the args every time.</td>
</tr>
<tr>
<td><b>%</b> gdb --args a.out 1 2 3
<b>(gdb)</b> run<br />
...
<b>(gdb)</b> run<br />
...</td>
<td><b>%</b> lldb -- a.out 1 2 3
<b>(lldb)</b> run<br />
...
<b>(lldb)</b> run<br />
...</td>
</tr>
<tr>
<td colspan="2">Or:</td>
</tr>
<tr>
<td><b>(gdb)</b> set args 1 2 3
<b>(gdb)</b> run<br />
...
<b>(gdb)</b> run<br />
...</td>
<td><b>(lldb)</b> settings set target.run-args 1 2 3
<b>(lldb)</b> run<br />
...
<b>(lldb)</b> run<br />
...</td>
</tr>
<tr>
<td colspan="2">Launch a process with arguments in new terminal window (Mac OS X only).</td>
</tr>
<tr>
<td></td>
<td><b>(lldb)</b> process launch --tty -- &lt;args&gt;
<b>(lldb)</b> pro la -t -- &lt;args&gt;</td>
</tr>
<tr>
<td colspan="2">Launch a process with arguments in existing terminal /dev/ttys006 (Mac OS X only).</td>
</tr>
<tr>
<td></td>
<td><b>(lldb)</b> process launch --tty=/dev/ttys006 -- &lt;args&gt;
<b>(lldb)</b> pro la -t/dev/ttys006 -- &lt;args&gt;</td>
</tr>
<tr>
<td colspan="2">Set environment variables for process before launching.</td>
</tr>
<tr>
<td><b>(gdb)</b> set env DEBUG 1</td>
<td><b>(lldb)</b> settings set target.env-vars DEBUG=1
<b>(lldb)</b> set se target.env-vars DEBUG=1
<b>(lldb)</b> env DEBUG=1</td>
</tr>
<tr>
<td colspan="2">Show the arguments that will be or were passed to the program when run.</td>
</tr>
<tr>
<td><b>(gdb)</b> show args<br />
Argument list to give program being debugged when it is started is "1 2 3".</td>
<td><b>(lldb)</b> settings show target.run-args<br />
target.run-args (array of strings) =<br />
[0]: "1"<br />
[1]: "2"<br />
[2]: "3"</td>
</tr>
<tr>
<td colspan="2">Set environment variables for process and launch process in one command.</td>
</tr>
<tr>
<td></td>
<td><b>(lldb)</b> process launch -v DEBUG=1</td>
</tr>
<tr>
<td colspan="2">Attach to a process with process ID 123.</td>
</tr>
<tr>
<td><b>(gdb)</b> attach 123</td>
<td><b>(lldb)</b> process attach --pid 123
<b>(lldb)</b> attach -p 123</td>
</tr>
<tr>
<td colspan="2">Attach to a process named "a.out".</td>
</tr>
<tr>
<td><b>(gdb)</b> attach a.out</td>
<td><b>(lldb)</b> process attach --name a.out
<b>(lldb)</b> pro at -n a.out</td>
</tr>
<tr>
<td colspan="2">Wait for a process named "a.out" to launch and attach.</td>
</tr>
<tr>
<td><b>(gdb)</b> attach -waitfor a.out</td>
<td><b>(lldb)</b> process attach --name a.out --waitfor
<b>(lldb)</b> pro at -n a.out -w</td>
</tr>
<tr>
<td colspan="2">Attach to a remote gdb protocol server running on system "eorgadd", port 8000.</td>
</tr>
<tr>
<td><b>(gdb)</b> target remote eorgadd:8000</td>
<td><b>(lldb)</b> gdb-remote eorgadd:8000</td>
</tr>
<tr>
<td colspan="2">Attach to a remote gdb protocol server running on the local system, port 8000.</td>
</tr>
<tr>
<td><b>(gdb)</b> target remote localhost:8000</td>
<td><b>(lldb)</b> gdb-remote 8000</td>
</tr>
<tr>
<td colspan="2">Attach to a Darwin kernel in kdp mode on system "eorgadd".</td>
</tr>
<tr>
<td><b>(gdb)</b> kdp-reattach eorgadd</td>
<td><b>(lldb)</b> kdp-remote eorgadd</td>
</tr>
<tr>
<td colspan="2">Do a source level single step in the currently selected thread.</td>
</tr>
<tr>
<td><b>(gdb)</b> step
<b>(gdb)</b> s</td>
<td><b>(lldb)</b> thread step-in
<b>(lldb)</b> step
<b>(lldb)</b> s</td>
</tr>
<tr>
<td colspan="2">Do a source level single step over in the currently selected thread.</td>
</tr>
<tr>
<td><b>(gdb)</b> next
<b>(gdb)</b> n</td>
<td><b>(lldb)</b> thread step-over
<b>(lldb)</b> next
<b>(lldb)</b> n</td>
</tr>
<tr>
<td colspan="2">Do an instruction level single step in the currently selected thread.</td>
</tr>
<tr>
<td><b>(gdb)</b> stepi
<b>(gdb)</b> si</td>
<td><b>(lldb)</b> thread step-inst
<b>(lldb)</b> si</td>
</tr>
<tr>
<td colspan="2">Do an instruction level single step over in the currently selected thread.</td>
</tr>
<tr>
<td><b>(gdb)</b> nexti
<b>(gdb)</b> ni</td>
<td><b>(lldb)</b> thread step-inst-over
<b>(lldb)</b> ni</td>
</tr>
<tr>
<td colspan="2">Step out of the currently selected frame.</td>
</tr>
<tr>
<td><b>(gdb)</b> finish</td>
<td><b>(lldb)</b> thread step-out
<b>(lldb)</b> finish</td>
</tr>
<tr>
<td colspan="2">Return immediately from the currently selected frame, with an optional return value.</td>
</tr>
<tr>
<td><b>(gdb)</b> return &lt;RETURN EXPRESSION&gt;</td>
<td><b>(lldb)</b> thread return &lt;RETURN EXPRESSION&gt;</td>
</tr>
<tr>
<td colspan="2">Backtrace and disassemble every time you stop.</td>
</tr>
<tr>
<td></td>
<td><b>(lldb)</b> target stop-hook add<br />
Enter your stop hook command(s). Type 'DONE' to end.<br />
&gt; bt<br />
&gt; disassemble --pc<br />
&gt; DONE<br />
Stop hook #1 added.</td>
</tr>
</tbody>
</table>
&nbsp;</p>

<p>
<div></div>
<h1>BREAKPOINT COMMANDS</h1>
<div /></p>

<p>&nbsp;
<table width="620" cellspacing="0">
<tbody>
<tr>
<td width="50%">GDB</td>
<td width="50%">LLDB</td>
</tr>
<tr>
<td colspan="2">Set a breakpoint at all functions named <b>main</b>.</td>
</tr>
<tr>
<td><b>(gdb)</b> break main</td>
<td><b>(lldb)</b> breakpoint set --name main
<b>(lldb)</b> br s -n main
<b>(lldb)</b> b main</td>
</tr>
<tr>
<td colspan="2">Set a breakpoint in file <b>test.c</b> at line <b>12</b>.</td>
</tr>
<tr>
<td><b>(gdb)</b> break test.c:12</td>
<td><b>(lldb)</b> breakpoint set --file test.c --line 12
<b>(lldb)</b> br s -f test.c -l 12
<b>(lldb)</b> b test.c:12</td>
</tr>
<tr>
<td colspan="2">Set a breakpoint at all C++ methods whose basename is <b>main</b>.</td>
</tr>
<tr>
<td><b>(gdb)</b> break main
<i>(Hope that there are no C funtions named <b>main</b>)</i>.</td>
<td><b>(lldb)</b> breakpoint set --method main
<b>(lldb)</b> br s -M main</td>
</tr>
<tr>
<td colspan="2">Set a breakpoint at and object C function: <b>-[NSString stringWithFormat:]</b>.</td>
</tr>
<tr>
<td><b>(gdb)</b> break -[NSString stringWithFormat:]</td>
<td><b>(lldb)</b> breakpoint set --name "-[NSString stringWithFormat:]"
<b>(lldb)</b> b -[NSString stringWithFormat:]</td>
</tr>
<tr>
<td colspan="2">Set a breakpoint at all Objective C methods whose selector is <b>count</b>.</td>
</tr>
<tr>
<td><b>(gdb)</b> break count
<i>(Hope that there are no C or C++ funtions named<b>count</b>)</i>.</td>
<td><b>(lldb)</b> breakpoint set --selector count
<b>(lldb)</b> br s -S count</td>
</tr>
<tr>
<td colspan="2">Set a breakpoint by regular expression on function name.</td>
</tr>
<tr>
<td><b>(gdb)</b> rbreak regular-expression</td>
<td><b>(lldb)</b> breakpoint set --func-regex regular-expression
<b>(lldb)</b> br s -r regular-expression</td>
</tr>
<tr>
<td colspan="2">Ensure that breakpoints by file and line work for #included .c/.cpp/.m files.</td>
</tr>
<tr>
<td><b>(gdb)</b> b foo.c:12</td>
<td><b>(lldb)</b> settings set target.inline-breakpoint-strategy always
<b>(lldb)</b> br s -f foo.c -l 12</td>
</tr>
<tr>
<td colspan="2">Set a breakpoint by regular expression on source file contents.</td>
</tr>
<tr>
<td><b>(gdb)</b> shell grep -e -n pattern source-file
<b>(gdb)</b> break source-file:CopyLineNumbers</td>
<td><b>(lldb)</b> breakpoint set --source-pattern regular-expression --file SourceFile
<b>(lldb)</b> br s -p regular-expression -f file</td>
</tr>
<tr>
<td colspan="2">List all breakpoints.</td>
</tr>
<tr>
<td><b>(gdb)</b> info break</td>
<td><b>(lldb)</b> breakpoint list
<b>(lldb)</b> br l</td>
</tr>
<tr>
<td colspan="2">Delete a breakpoint.</td>
</tr>
<tr>
<td><b>(gdb)</b> delete 1</td>
<td><b>(lldb)</b> breakpoint delete 1
<b>(lldb)</b> br del 1</td>
</tr>
</tbody>
</table>
&nbsp;</p>

<p>
<div></div>
<h1>WATCHPOINT COMMANDS</h1>
<div /></p>

<p>&nbsp;
<table width="620" cellspacing="0">
<tbody>
<tr>
<td width="50%">GDB</td>
<td width="50%">LLDB</td>
</tr>
<tr>
<td colspan="2">Set a watchpoint on a variable when it is written to.</td>
</tr>
<tr>
<td><b>(gdb)</b> watch global_var</td>
<td><b>(lldb)</b> watchpoint set variable global_var
<b>(lldb)</b> wa s v global_var</td>
</tr>
<tr>
<td colspan="2">Set a watchpoint on a memory location when it is written into. The size of the region to watch for defaults to the pointer size if no '-x byte_size' is specified. This command takes raw input, evaluated as an expression returning an unsigned integer pointing to the start of the region, after the '--' option terminator.</td>
</tr>
<tr>
<td><b>(gdb)</b> watch -location g_char_ptr</td>
<td><b>(lldb)</b> watchpoint set expression -- my_ptr
<b>(lldb)</b> wa s e -- my_ptr</td>
</tr>
<tr>
<td colspan="2">Set a condition on a watchpoint.</td>
</tr>
<tr>
<td></td>
<td><b>(lldb)</b> watch set var global
<b>(lldb)</b> watchpoint modify -c '(global==5)'
<b>(lldb)</b> c<br />
...
<b>(lldb)</b> bt<br />
* thread #1: tid = 0x1c03, 0x0000000100000ef5 a.out`modify + 21 at main.cpp:16, stop reason = watchpoint 1<br />
frame #0: 0x0000000100000ef5 a.out`modify + 21 at main.cpp:16<br />
frame #1: 0x0000000100000eac a.out`main + 108 at main.cpp:25<br />
frame #2: 0x00007fff8ac9c7e1 libdyld.dylib`start + 1
<b>(lldb)</b> frame var global<br />
(int32_t) global = 5</td>
</tr>
<tr>
<td colspan="2">List all watchpoints.</td>
</tr>
<tr>
<td><b>(gdb)</b> info break</td>
<td><b>(lldb)</b> watchpoint list
<b>(lldb)</b> watch l</td>
</tr>
<tr>
<td colspan="2">Delete a watchpoint.</td>
</tr>
<tr>
<td><b>(gdb)</b> delete 1</td>
<td><b>(lldb)</b> watchpoint delete 1
<b>(lldb)</b> watch del 1</td>
</tr>
</tbody>
</table>
&nbsp;</p>

<p>
<div></div>
<h1>EXAMINING VARIABLES</h1>
<div /></p>

<p>&nbsp;
<table width="620" cellspacing="0">
<tbody>
<tr>
<td width="50%">GDB</td>
<td width="50%">LLDB</td>
</tr>
<tr>
<td colspan="2">Show the arguments and local variables for the current frame.</td>
</tr>
<tr>
<td><b>(gdb)</b> info args<br />
and
<b>(gdb)</b> info locals</td>
<td><b>(lldb)</b> frame variable
<b>(lldb)</b> fr v</td>
</tr>
<tr>
<td colspan="2">Show the local variables for the current frame.</td>
</tr>
<tr>
<td><b>(gdb)</b> info locals</td>
<td><b>(lldb)</b> frame variable --no-args
<b>(lldb)</b> fr v -a</td>
</tr>
<tr>
<td colspan="2">Show the contents of local variable "bar".</td>
</tr>
<tr>
<td><b>(gdb)</b> p bar</td>
<td><b>(lldb)</b> frame variable bar
<b>(lldb)</b> fr v bar
<b>(lldb)</b> p bar</td>
</tr>
<tr>
<td colspan="2">Show the contents of local variable "bar" formatted as hex.</td>
</tr>
<tr>
<td><b>(gdb)</b> p/x bar</td>
<td><b>(lldb)</b> frame variable --format x bar
<b>(lldb)</b> fr v -f x bar</td>
</tr>
<tr>
<td colspan="2">Show the contents of global variable "baz".</td>
</tr>
<tr>
<td><b>(gdb)</b> p baz</td>
<td><b>(lldb)</b> target variable baz
<b>(lldb)</b> ta v baz</td>
</tr>
<tr>
<td colspan="2">Show the global/static variables defined in the current source file.</td>
</tr>
<tr>
<td>n/a</td>
<td><b>(lldb)</b> target variable
<b>(lldb)</b> ta v</td>
</tr>
<tr>
<td colspan="2">Display a the variable "argc" and "argv" every time you stop.</td>
</tr>
<tr>
<td><b>(gdb)</b> display argc
<b>(gdb)</b> display argv</td>
<td><b>(lldb)</b> target stop-hook add --one-liner "frame variable argc argv"
<b>(lldb)</b> ta st a -o "fr v argc argv"
<b>(lldb)</b> display argc
<b>(lldb)</b> display argv</td>
</tr>
<tr>
<td colspan="2">Display a the variable "argc" and "argv" only when you stop in the function named <b>main</b>.</td>
</tr>
<tr>
<td></td>
<td><b>(lldb)</b> target stop-hook add --name main --one-liner "frame variable argc argv"
<b>(lldb)</b> ta st a -n main -o "fr v argc argv"</td>
</tr>
<tr>
<td colspan="2">Display the variable "*this" only when you stop in c class named <b>MyClass</b>.</td>
</tr>
<tr>
<td></td>
<td><b>(lldb)</b> target stop-hook add --classname MyClass --one-liner "frame variable *this"
<b>(lldb)</b> ta st a -c MyClass -o "fr v *this"</td>
</tr>
</tbody>
</table>
&nbsp;</p>

<p>
<h1>EVALUATING EXPRESSIONS</h1>
<div /></p>

<p>&nbsp;
<table width="620" cellspacing="0">
<tbody>
<tr>
<td width="50%">GDB</td>
<td width="50%">LLDB</td>
</tr>
<tr>
<td colspan="2">Evaluating a generalized expression in the current frame.</td>
</tr>
<tr>
<td><b>(gdb)</b> print (int) printf ("Print nine: %d.", 4 + 5)<br />
or if you don't want to see void returns:
<b>(gdb)</b> call (int) printf ("Print nine: %d.", 4 + 5)</td>
<td><b>(lldb)</b> expr (int) printf ("Print nine: %d.", 4 + 5)<br />
or using the print alias:
<b>(lldb)</b> print (int) printf ("Print nine: %d.", 4 + 5)</td>
</tr>
<tr>
<td colspan="2">Creating and assigning a value to a convenience variable.</td>
</tr>
<tr>
<td><b>(gdb)</b> set $foo = 5
<b>(gdb)</b> set variable $foo = 5<br />
or using the print command
<b>(gdb)</b> print $foo = 5<br />
or using the call command
<b>(gdb)</b> call $foo = 5<br />
and if you want to specify the type of the variable:<b>(gdb)</b> set $foo = (unsigned int) 5</td>
<td>In lldb you evaluate a variable declaration expression as you would write it in C:
<b>(lldb)</b> expr unsigned int $foo = 5</td>
</tr>
<tr>
<td colspan="2">Printing the ObjC "description" of an object.</td>
</tr>
<tr>
<td><b>(gdb)</b> po [SomeClass returnAnObject]</td>
<td><b>(lldb)</b> expr -o -- [SomeClass returnAnObject]<br />
or using the po alias:
<b>(lldb)</b> po [SomeClass returnAnObject]</td>
</tr>
<tr>
<td colspan="2">Print the dynamic type of the result of an expression.</td>
</tr>
<tr>
<td><b>(gdb)</b> set print object 1
<b>(gdb)</b> p someCPPObjectPtrOrReference<br />
only works for C++ objects.</td>
<td><b>(lldb)</b> expr -d 1 -- [SomeClass returnAnObject]
<b>(lldb)</b> expr -d 1 -- someCPPObjectPtrOrReference<br />
or set dynamic type printing to be the default: <b>(lldb)</b>settings set target.prefer-dynamic run-target</td>
</tr>
<tr>
<td colspan="2">Calling a function so you can stop at a breakpoint in the function.</td>
</tr>
<tr>
<td><b>(gdb)</b> set unwindonsignal 0
<b>(gdb)</b> p function_with_a_breakpoint()</td>
<td><b>(lldb)</b> expr -i 0 -- function_with_a_breakpoint()</td>
</tr>
<tr>
<td colspan="2">Calling a function that crashes, and stopping when the function crashes.</td>
</tr>
<tr>
<td><b>(gdb)</b> set unwindonsignal 0
<b>(gdb)</b> p function_which_crashes()</td>
<td><b>(lldb)</b> expr -u 0 -- function_which_crashes()</td>
</tr>
</tbody>
</table>
&nbsp;</p>

<p>
<h1>EXAMINING THREAD STATE</h1>
<div /></p>

<p>&nbsp;
<table width="620" cellspacing="0">
<tbody>
<tr>
<td width="50%">GDB</td>
<td width="50%">LLDB</td>
</tr>
<tr>
<td colspan="2">Show the stack backtrace for the current thread.</td>
</tr>
<tr>
<td><b>(gdb)</b> bt</td>
<td><b>(lldb)</b> thread backtrace
<b>(lldb)</b> bt</td>
</tr>
<tr>
<td colspan="2">Show the stack backtraces for all threads.</td>
</tr>
<tr>
<td><b>(gdb)</b> thread apply all bt</td>
<td><b>(lldb)</b> thread backtrace all
<b>(lldb)</b> bt all</td>
</tr>
<tr>
<td colspan="2">Backtrace the first five frames of the current thread.</td>
</tr>
<tr>
<td><b>(gdb)</b> bt 5</td>
<td><b>(lldb)</b> thread backtrace -c 5
<b>(lldb)</b> bt 5 (<i>lldb-169 and later</i>)
<b>(lldb)</b> bt -c 5 (<i>lldb-168 and earlier</i>)</td>
</tr>
<tr>
<td colspan="2">Select a different stack frame by index for the current thread.</td>
</tr>
<tr>
<td><b>(gdb)</b> frame 12</td>
<td><b>(lldb)</b> frame select 12
<b>(lldb)</b> fr s 12
<b>(lldb)</b> f 12</td>
</tr>
<tr>
<td colspan="2">List information about the currently selected frame in the current thread.</td>
</tr>
<tr>
<td></td>
<td><b>(lldb)</b> frame info</td>
</tr>
<tr>
<td colspan="2">Select the stack frame that called the current stack frame.</td>
</tr>
<tr>
<td><b>(gdb)</b> up</td>
<td><b>(lldb)</b> up
<b>(lldb)</b> frame select --relative=1</td>
</tr>
<tr>
<td colspan="2">Select the stack frame that is called by the current stack frame.</td>
</tr>
<tr>
<td><b>(gdb)</b> down</td>
<td><b>(lldb)</b> down
<b>(lldb)</b> frame select --relative=-1
<b>(lldb)</b> fr s -r-1</td>
</tr>
<tr>
<td colspan="2">Select a different stack frame using a relative offset.</td>
</tr>
<tr>
<td><b>(gdb)</b> up 2
<b>(gdb)</b> down 3</td>
<td><b>(lldb)</b> frame select --relative 2
<b>(lldb)</b> fr s -r2</td></tr></tbody></table></p>

<p><b>(lldb)</b> frame select --relative -3
<b>(lldb)</b> fr s -r-3

<tr>
<td colspan="2">Show the general purpose registers for the current thread.</td>
</tr>
<tr>
<td><b>(gdb)</b> info registers</td>
<td><b>(lldb)</b> register read</td>
</tr>
<tr>
<td colspan="2">Write a new decimal value '123' to the current thread register 'rax'.</td>
</tr>
<tr>
<td><b>(gdb)</b> p $rax = 123</td>
<td><b>(lldb)</b> register write rax 123</td>
</tr>
<tr>
<td colspan="2">Skip 8 bytes ahead of the current program counter (instruction pointer). Note that we use backticks to evaluate an expression and insert the scalar result in LLDB.</td>
</tr>
<tr>
<td><b>(gdb)</b> jump *$pc+8</td>
<td><b>(lldb)</b> register write pc `$pc+8`</td>
</tr>
<tr>
<td colspan="2">Show the general purpose registers for the current thread formatted as <b>signed decimal</b>. LLDB tries to use the same format characters as <b>printf(3)</b> when possible. Type "help format" to see the full list of format specifiers.</td>
</tr>
<tr>
<td></td>
<td><b>(lldb)</b> register read --format i
<b>(lldb)</b> re r -f i</td></tr></p>

<p><i>LLDB now supports the GDB shorthand format syntax but there can't be space after the command:</i>
<b>(lldb)</b> register read/d

<tr>
<td colspan="2">Show all registers in all register sets for the current thread.</td>
</tr>
<tr>
<td><b>(gdb)</b> info all-registers</td>
<td><b>(lldb)</b> register read --all
<b>(lldb)</b> re r -a</td>
</tr>
<tr>
<td colspan="2">Show the values for the registers named "rax", "rsp" and "rbp" in the current thread.</td>
</tr>
<tr>
<td><b>(gdb)</b> info all-registers rax rsp rbp</td>
<td><b>(lldb)</b> register read rax rsp rbp</td>
</tr>
<tr>
<td colspan="2">Show the values for the register named "rax" in the current thread formatted as <b>binary</b>.</td>
</tr>
<tr>
<td><b>(gdb)</b> p/t $rax</td>
<td><b>(lldb)</b> register read --format binary rax
<b>(lldb)</b> re r -f b rax</td></tr></p>

<p><i>LLDB now supports the GDB shorthand format syntax but there can't be space after the command:</i>
<b>(lldb)</b> register read/t rax
<b>(lldb)</b> p/t $rax

<tr>
<td colspan="2">Read memory from address 0xbffff3c0 and show 4 hex uint32_t values.</td>
</tr>
<tr>
<td><b>(gdb)</b> x/4xw 0xbffff3c0</td>
<td><b>(lldb)</b> memory read --size 4 --format x --count 4 0xbffff3c0
<b>(lldb)</b> me r -s4 -fx -c4 0xbffff3c0
<b>(lldb)</b> x -s4 -fx -c4 0xbffff3c0</td></tr></p>

<p><i>LLDB now supports the GDB shorthand format syntax but there can't be space after the command:</i>
<b>(lldb)</b> memory read/4xw 0xbffff3c0
<b>(lldb)</b> x/4xw 0xbffff3c0
<b>(lldb)</b> memory read --gdb-format 4xw 0xbffff3c0

<tr>
<td colspan="2">Read memory starting at the expression "argv[0]".</td>
</tr>
<tr>
<td><b>(gdb)</b> x argv[0]</td>
<td><b>(lldb)</b> memory read `argv[0]`
<i><b>NOTE:</b> any command can inline a scalar expression result (as long as the target is stopped) using backticks around any expression:</i>
<b>(lldb)</b> memory read --size `sizeof(int)` `argv[0]`</td>
</tr>
<tr>
<td colspan="2">Read 512 bytes of memory from address 0xbffff3c0 and save results to a local file as <b>text</b>.</td>
</tr>
<tr>
<td><b>(gdb)</b> set logging on
<b>(gdb)</b> set logging file /tmp/mem.txt
<b>(gdb)</b> x/512bx 0xbffff3c0
<b>(gdb)</b> set logging off</td>
<td><b>(lldb)</b> memory read --outfile /tmp/mem.txt --count 512 0xbffff3c0
<b>(lldb)</b> me r -o/tmp/mem.txt -c512 0xbffff3c0
<b>(lldb)</b> x/512bx -o/tmp/mem.txt 0xbffff3c0</td>
</tr>
<tr>
<td colspan="2">Save binary memory data starting at 0x1000 and ending at 0x2000 to a file.</td>
</tr>
<tr>
<td><b>(gdb)</b> dump memory /tmp/mem.bin 0x1000 0x2000</td>
<td><b>(lldb)</b> memory read --outfile /tmp/mem.bin --binary 0x1000 0x1200
<b>(lldb)</b> me r -o /tmp/mem.bin -b 0x1000 0x1200</td>
</tr>
<tr>
<td colspan="2">Get information about a specific heap allocation (available on Mac OS X only).</td>
</tr>
<tr>
<td><b>(gdb)</b> info malloc 0x10010d680</td>
<td><b>(lldb)</b> command script import lldb.macosx.heap
<b>(lldb)</b> process launch --environment MallocStackLogging=1 -- [ARGS]
<b>(lldb)</b> malloc_info --stack-history 0x10010d680</td>
</tr>
<tr>
<td colspan="2">Get information about a specific heap allocation and cast the result to any dynamic type that can be deduced (available on Mac OS X only)</td>
</tr>
<tr>
<td></td>
<td><b>(lldb)</b> command script import lldb.macosx.heap
<b>(lldb)</b> malloc_info --type 0x10010d680</td>
</tr>
<tr>
<td colspan="2">Find all heap blocks that contain a pointer specified by an expression EXPR (available on Mac OS X only).</td>
</tr>
<tr>
<td></td>
<td><b>(lldb)</b> command script import lldb.macosx.heap
<b>(lldb)</b> ptr_refs EXPR</td>
</tr>
<tr>
<td colspan="2">Find all heap blocks that contain a C string anywhere in the block (available on Mac OS X only).</td>
</tr>
<tr>
<td></td>
<td><b>(lldb)</b> command script import lldb.macosx.heap
<b>(lldb)</b> cstr_refs CSTRING</td>
</tr>
<tr>
<td colspan="2">Disassemble the current function for the current frame.</td>
</tr>
<tr>
<td><b>(gdb)</b> disassemble</td>
<td><b>(lldb)</b> disassemble --frame
<b>(lldb)</b> di -f</td>
</tr>
<tr>
<td colspan="2">Disassemble any functions named <b>main</b>.</td>
</tr>
<tr>
<td><b>(gdb)</b> disassemble main</td>
<td><b>(lldb)</b> disassemble --name main
<b>(lldb)</b> di -n main</td>
</tr>
<tr>
<td colspan="2">Disassemble an address range.</td>
</tr>
<tr>
<td><b>(gdb)</b> disassemble 0x1eb8 0x1ec3</td>
<td><b>(lldb)</b> disassemble --start-address 0x1eb8 --end-address 0x1ec3
<b>(lldb)</b> di -s 0x1eb8 -e 0x1ec3</td>
</tr>
<tr>
<td colspan="2">Disassemble 20 instructions from a given address.</td>
</tr>
<tr>
<td><b>(gdb)</b> x/20i 0x1eb8</td>
<td><b>(lldb)</b> disassemble --start-address 0x1eb8 --count 20
<b>(lldb)</b> di -s 0x1eb8 -c 20</td>
</tr>
<tr>
<td colspan="2">Show mixed source and disassembly for the current function for the current frame.</td>
</tr>
<tr>
<td>n/a</td>
<td><b>(lldb)</b> disassemble --frame --mixed
<b>(lldb)</b> di -f -m</td>
</tr>
<tr>
<td colspan="2">Disassemble the current function for the current frame and show the opcode bytes.</td>
</tr>
<tr>
<td>n/a</td>
<td><b>(lldb)</b> disassemble --frame --bytes
<b>(lldb)</b> di -f -b</td>
</tr>
<tr>
<td colspan="2">Disassemble the current source line for the current frame.</td>
</tr>
<tr>
<td>n/a</td>
<td><b>(lldb)</b> disassemble --line
<b>(lldb)</b> di -l</td>
</tr>


&nbsp;</p>

<p>
<div></div>
<h1>EXECUTABLE AND SHARED LIBRARY QUERY COMMANDS</h1>
<div /></p>

<p>&nbsp;
<table width="620" cellspacing="0">
<tbody>
<tr>
<td width="50%">GDB</td>
<td width="50%">LLDB</td>
</tr>
<tr>
<td colspan="2">List the main executable and all dependent shared libraries.</td>
</tr>
<tr>
<td><b>(gdb)</b> info shared</td>
<td><b>(lldb)</b> image list</td>
</tr>
<tr>
<td colspan="2">Look up information for a raw address in the executable or any shared libraries.</td>
</tr>
<tr>
<td><b>(gdb)</b> info symbol 0x1ec4</td>
<td><b>(lldb)</b> image lookup --address 0x1ec4
<b>(lldb)</b> im loo -a 0x1ec4</td>
</tr>
<tr>
<td colspan="2">Look up functions matching a regular expression in a binary.</td>
</tr>
<tr>
<td><b>(gdb)</b> info function &lt;FUNC_REGEX&gt;</td>
<td>This one finds debug symbols:
<b>(lldb)</b> image lookup -r -n &lt;FUNC_REGEX&gt;</td></tr></tbody></table></p>

<p>This one finds non-debug symbols:
<b>(lldb)</b> image lookup -r -s &lt;FUNC_REGEX&gt;</p>

<p>Provide a list of binaries as arguments to limit the search.

<tr>
<td colspan="2">Find full souce line information.</td>
</tr>
<tr>
<td><b>(gdb)</b> info line 0x1ec4</td>
<td>This one is a bit messy at present. Do:</td></tr></p>

<p><b>(lldb)</b> image lookup -v --address 0x1ec4</p>

<p>and look for the LineEntry line, which will have the full source path and line range information.

<tr>
<td colspan="2">Look up information for an address in <b>a.out</b> only.</td>
</tr>
<tr>
<td></td>
<td><b>(lldb)</b> image lookup --address 0x1ec4 a.out
<b>(lldb)</b> im loo -a 0x1ec4 a.out</td>
</tr>
<tr>
<td colspan="2">Look up information for for a type <code>Point</code> by name.</td>
</tr>
<tr>
<td><b>(gdb)</b> ptype Point</td>
<td><b>(lldb)</b> image lookup --type Point
<b>(lldb)</b> im loo -t Point</td>
</tr>
<tr>
<td colspan="2">Dump all sections from the main executable and any shared libraries.</td>
</tr>
<tr>
<td><b>(gdb)</b> maintenance info sections</td>
<td><b>(lldb)</b> image dump sections</td>
</tr>
<tr>
<td colspan="2">Dump all sections in the <b>a.out</b> module.</td>
</tr>
<tr>
<td></td>
<td><b>(lldb)</b> image dump sections a.out</td>
</tr>
<tr>
<td colspan="2">Dump all symbols from the main executable and any shared libraries.</td>
</tr>
<tr>
<td></td>
<td><b>(lldb)</b> image dump symtab</td>
</tr>
<tr>
<td colspan="2">Dump all symbols in <b>a.out</b> and <b>liba.so</b>.</td>
</tr>
<tr>
<td></td>
<td><b>(lldb)</b> image dump symtab a.out liba.so</td>
</tr>


&nbsp;</p>

<p>
<div></div>
<h1>MISCELLANEOUS</h1>
<div /></p>

<p>&nbsp;
<table width="620" cellspacing="0">
<tbody>
<tr>
<td width="50%">GDB</td>
<td width="50%">LLDB</td>
</tr>
<tr>
<td colspan="2">Echo text to the screen.</td>
</tr>
<tr>
<td><b>(gdb)</b> echo Here is some text\n</td>
<td><b>(lldb)</b> script print "Here is some text"</td>
</tr>
<tr>
<td colspan="2">Remap source file pathnames for the debug session. If your source files are no longer located in the same location as when the program was built --- maybe the program was built on a different computer --- you need to tell the debugger how to find the sources at their local file path instead of the build system's file path.</td>
</tr>
<tr>
<td><b>(gdb)</b> set pathname-substitutions /buildbot/path /my/path</td>
<td><b>(lldb)</b> settings set target.source-map /buildbot/path /my/path</td>
</tr>
<tr>
<td colspan="2">Supply a catchall directory to search for source files in.</td>
</tr>
<tr>
<td><b>(gdb)</b> directory /my/path</td>
<td>(<i>No equivalent command - use the source-map instead.)
</i></td>
</tr>
</tbody>
</table>
</p>
