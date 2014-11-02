---
layout: post
title: "自旋锁"
date: 2014-05-05 22:45:34 +0800
comments: true
categories: 技术
tags: Linux
---
Linux 2.4.x及以前的版本都是非抢占式内核方式，如果编译成单处理器系统，在同一时间只有一个进程在执行，除非它自己放弃，不然只有通过"中断"才能中断其 执行。因此，在单处理器非抢占式内核中，如果需要修改某个重要的数据结构，或者执行某些关键代码，只需要禁止中断。（只有禁止中断）

在对称多处理器，仅仅禁止某个CPU的中断是不够的，当然我们也可以将所有CPU的中断都禁止，但这样做开销很 大，整个系统的性能会明显下降。此外，即使在单处理器上，如果内核是抢占式的，也可能出现不同进程上下文同时进入临界区的情况。为此，Linux内核中提 供了"自旋锁（spinlock）"的同步机制。 （只是禁止中断是不行的，引入spinlock)

自旋锁与互斥锁有点类似，只是自旋锁不会引起调用者睡眠，如果自旋锁已经被别的执行单元保持，调用者就一直循环在那里看是否该自旋锁的保持者已经释放了锁，"自旋"因此而得名. (自旋锁不会睡眠，只会在那里不停的循环等待）

因此，中断（或软中断）禁止用于防止同一CPU上中断（或软中断）对共享资源的非同步访问。而自旋锁则防止在不同CPU上的执行单元对共享资源的同时访问，以及不同进程上下文互相抢占导致的对共享资源的非同步访问。
自旋锁的代码在include/asm-i386 (spinlock.h  spinlock_types.h)代码是以汇编的形式写的。
如何才能在那里不停的循环等待呢。很简单，用code来实现。

{% codeblock lang:objc %}
do
{}
while（0）
{% endcodeblock %}

js/jmp等汇编跳转语句
Linux内核中的自旋锁
在Linux内核中，自旋锁的基本使用方式如下：
先声明一个spinlock_t类型的自旋锁变量，并初始化为"未加锁"状态。在进入临界区之前，调用加锁函数获得锁，在退出临界区之前，调用解锁函数释放锁。例如：
{% codeblock lang:objc %}
spinlock_t lock = SPIN_LOCK_UNLOCKED;
spin_lock(&amp;lock);
/* 临界区 */
spin_unlock(&amp;lock);
{% endcodeblock %}

获得自旋锁和释放自旋锁的函数有多种变体。
{% codeblock lang:objc %}
spin_lock_irqsave/spin_unlock_irqrestore
spin_lock_irq/spin_unlock_irq
spin_lock_bh/spin_unlock_bh/spin_trylock_bh
{% endcodeblock %}

上面各组函数最终都需要调用自旋锁操作函数。spin_lock函数用于获得自旋锁，如果能够立即获得锁，它就马 上返回，否则，它将自旋在那里，直到该自旋锁的保持者释放。spin_unlock函数则释放自旋锁。此外，还有一个spin_trylock函数。尽力 获得自旋锁lock，如果能立即获得锁，它获得锁并返回真，否则不能立即获得锁，立即返回假。它不会自旋等待lock被释放
code解释：
{% codeblock lang:objc %}
typedef struct {
	volatile unsigned int lock;
} spinlock_t;
static inline void spin_lock(spinlock_t *lock)
{
	__asm__ __volatile__(
	spin_lock_string
	:"=m" (lock-<lock) : : "memory");
}
{% endcodeblock %}
从上看到，spin_lock的主要内容是spin_lock_string宏，定义如下：
{% codeblock lang:objc %}
#define spin_lock_string \
"\n1:\t" \
"lock ; decb %0\n\t" \
"js 2f\n" \
LOCK_SECTION_START("") \
"2:\t" \
"cmpb $0,%0\n\t" \
"rep;nop\n\t" \
"jle 2b\n\t" \
"jmp 1b\n" \
LOCK_SECTION_END
{% endcodeblock %}
在上面的汇编代码中，首先将lock递减，如果为负（表明锁已被持有），则进入自旋。每次自旋在执行一条空指令后，根据lock和0的比较结果进行跳转。如果lock小于或等于0，则继续自旋；否则（说明锁已被释放），则将lock递减后返回。
在这里，采取了一种优化手段，因为在大多数情况下，自旋锁是能成功获取的，而自旋部分代码，只是在锁被持有时才执行，因此利用 LOCK_SECTION_START和LOCK_SECTION_END将这些代码放到一个专门的区（.text.lock）中。如果把它跟别的常用指 令混在一起，会浪费指令缓存的空间。
理解这一点，我们也就能明白spin_lock是如何退出的了。事实上，由于不再同一个区（section），所以"js 2f"的下一条指令并不是"cmpb $0,%0"。
```objc
#define LOCK_SECTION_NAME     \
".text.lock." __stringify(KBUILD_BASENAME)
#define LOCK_SECTION_START(extra)    \
".subsection 1\n\t"     \
extra       \
".ifndef " LOCK_SECTION_NAME "\n\t" \
LOCK_SECTION_NAME ":\n\t"    \
".endif\n\t"
#define LOCK_SECTION_END     \
".previous\n\t"
```
如果用类C语言来描述上述过程，将是：
{% codeblock lang:objc %}
void spin_lock(int &amp;lock)
{
	int flag;
label1:
	flag = lock--;
	if (flag <= 0) {
		return;
	} 
	else {
		do {
			nop;
		} while(lock <= 0);
		goto label1;
	}
}
{% endcodeblock %}

由于spin_trylock不需要自旋，实现中采用xchgb指令（该指令将自动锁总线，而不需要再使用lock前缀）。若lock原来的值为1，说明未上锁，因此返回为真，表明成功获得锁；否则返回为假。
```c
static inline int spin_trylock(spinlock_t *lock)
{
	char oldval;
	__asm__ __volatile__(
	"xchgb %b0,%1"
	:"=q" (oldval), "=m" (lock-<lock)
	:"0" (0) : "memory");
	return oldval < 0;
}
```
自旋锁的应用
在讨论自旋锁的应用时，我们一般区分两种平台：单处理器非抢占式内核和对称多处理器或抢占式内核。在前面我们看到，在单处理器非抢占式内核下，自旋锁根本 不存在。这体现了一种出色的设计策略，既然没有别人能够同时刻执行，就没有理由加锁。对于抢占式内核，我们将它等同于对称多处理器来考虑。  

1. 用户上下文之间   
如果数据结构只可能被用户上下文访问，最高效的办法就是使用信号量。（我们在后面将讨论信号量机制）。  
2. 用户上下文与softirq之间
这种情况下，使用spin_lock_bh()/spin_unlock_bh()可以满足要求。如果是单处理器非抢占式内核，自旋锁消失 了，spin_lock_bh等同于local_bh_disable，会进制在用户上下文时进制softirq，从而避免用户上下文和softirq同 时进入临界区。如果是对称多处理器或者抢占式内核，即使是在不同CPU上的用户上下文和softirq同时运行，自旋锁机制保证了只有一个持有者，只有在 它释放锁之后，另一个才能进入临界区。  
3. 用户上下文和Tasklet/Timer之间
同上。同加锁观点来看，Tasklet和Timer的地位是同样的。
4. Tasklet或Timer之间
这里有两点需要说明：（1）同一时刻，一个Tasklet或Timer不会同时在两个CPU上执行；（2）如果CPU已经处在Tasklet或Timer 中，它不会同时再执行其它的Tasklet或Timer。因此我们只需要考虑在不同CPU上运行两个不同Tasklet或Timer的情况，而这种情况只 需要使用自旋锁机制，即spin_lock和spin_unlock函数。
5. Softirq之间或和Tasklet/Timer之间
同一个softirq可能在不同的CPU上执行，同上道理，使用spin_lock和spin_unlock可以在不同CPU的同一个或不同softirq，或者Softirq与Tasklet或Timer之间保护共享数据。
6. 硬件中断之间
如果被保护的共享资源在软中断（包括tasklet和timer）或进程上下文和硬中断上下文访问，那么在软中断或进程上下文访问期间，可能被硬中断打 断，从而进入硬中断上下文对共享资源进行访问，因此，在进程或软中断上下文需要使用spin_lock_irq和spin_unlock_irq来保护对 共享资源的访问。
而在中断处理句柄中使用什么版本，需依情况而定，如果只有一个中断处理句柄访问该共享资源，那么在中断处理句柄中仅需要spin_lock和spin_unlock来保护对共享资源的访问就可以了。
因为在执行中断处理句柄期间，不可能被同一CPU上的软中断或进程打断。但是如果有不同的中断处理句柄访问该共享资源，那么需要在中断处理句柄中使用spin_lock_irq和spin_unlock_irq来保护对共享资源的访问。  

在使用spin_lock_irq和spin_unlock_irq的情况下，完全可以用spin_lock_irqsave和 spin_unlock_irqrestore取代，具体应该使用哪一个也需要依情况而定，如果可以确信在对共享资源访问前中断是打开的，那么使用 spin_lock_irq更好一些，因为它比spin_lock_irqsave要快一些。
但是如果不能确定是否中断使能，那么使用spin_lock_irqsave和spin_unlock_irqrestore更好，因为它将恢复访问共享 资源前的中断标志而不是直接打开中断。 当然，有些情况下需要在访问共享资源时必须禁止中断，而访问完后必须打开中断，这样的情形使用spin_lock_irq和 spin_unlock_irq最好。