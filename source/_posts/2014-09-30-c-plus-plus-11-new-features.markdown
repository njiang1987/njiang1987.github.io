---
layout: post
title: "C++ Primer 读书笔记"
date: 2014-09-30 16:29:22 +0800
comments: true
categories: C++
---
###1. Array

```cpp
	array<double, 4> a3 = {3.14, 2.72, 1.62, 1.41};
    array<double, 4> a4;
    a4 = a3;
```

###2. cin

```cpp
	getline(cin, first_name);
	cin.getline(first_name, 20);
```

###3. File - fstream
	
1. 包含头文件fstream
2. 创建一个ofstream对象
3. 将该ofstream对象同一个文件关联起来
4. 就像使用cout那样使用该ofstream对象

```cpp
	ofstream outFile;
    outFile.open("fish.txt");
    string filename;
    getline(cin, filename);
    outFile<<filename;
    outFile.close();
    ifstream inFile;
    inFile.open("fish.txt");
    string resultname;
    getline(inFile, resultname);
    cout<<resultname;
    inFile.close();
```

###4. 在函数传参过程中，尽量使用const
	
1. 这样可以避免由于五一间修改数据而导致的编程错误，
2. 使用const使得函数能够处理const 和非const 实参，否则将只能接受非const数据。

###5. 声明函数指针

```cpp
	double betsy(int);
	double pam1(int);
	void estimate(int lines, double (*pf)(int));
	double betsy(int lns)
	{
	    return 0.05*lns;
	}

	double pam1(int lns)
	{
	    return 0.03*lns + lns;
	}

	void estimate(int lines, double (*pf)(int))
	{
	    cout<<lines<<" lines will take ";
	    cout<<(*pf)(lines)<<" hour(s)\n";
	}

	int code;
    cout<<"how many lines?";
    cin>>code;
    cout<<"betsy estimate::";
    estimate(code, betsy);
    cout<<"pam1 estimate::";
    estimate(code, pam1);
```

###6. cout.precision(2)

###7. 显示具体化

```cpp
	template <> void swap<Job>(Job& a, Job& b)
	{
	    double t1;
	    int t2;
	    t1 = a.salary;
	    a.salary = b.salary;
	    b.salary = t1;
	    t2 = a.floor;
	    a.floor = b.floor;
	    b.floor = t2;
	}
```

###8. 关键字decltype 

```cpp
	int x;
	decltype(x) y; //将x的类型复制给y
```

给decltype提供的参数可以是表达式，编译器遍历一个核对表来实现声明.

###9. 声明和定义函数的语法

```cpp
	double h(int x, float y);
	auto h(int x, float y) -> double
```

###10. 在同一个文件中只能讲同一个头文件包含一次

```cpp
	#ifndef COORDIN_H_
	#define COORDIN_H_
	...
	#endif
```

###11. 名词修饰

重载函数，编译时， 名称修饰
	
```cpp
	long MyFunctionFoo(int, float)
	MyFunctionFoo@@YAXH
```

###12. thread_local 变量的声明周期与所属的线程一样长

###13. register 使用CPU寄存器来存储变量
	
`register int count_fast;`

###14. 未解决c++查抄c里面的函数原型问题

```cpp
	extern "C" void spiff(int);// use c protocol for name look-up
	extern void spoff(int);	//use c++ protocol for name look-up
	extern "C++" void spaff(int);	//use c++ protocol for name look-up
```

###15. int * pi = new int;
	int * pi = new int(sizeof(int));
	delete pi;
	delete (pi);

###16. 作用域内枚举 C++11, (struct)

```cpp
	enum class egg {Small, Medium, Large, Jumbo};
	enum class shirt {Small, Medium, Large, Jumbo};
	egg choise = egg::Large;
    shirt floyd = shirt::Large;
```

###17. 转换函数

```cpp
	operator double();
	Stonewt wolfe(285.7);
    double host = double (wolfe);
    double thinker = (double) wolfe;
```

1. 转换函数必须是类方法
2. 转换函数不能指定返回类型
3. 转换函数不能有参数

可以在声明构造函数时使用关键字`explicit`, 以防止它被用于隐式转换

###18. C++11 空指针

引入新关键字`nullptr`用于表示空指针

###19. 静态成员函数
 
```cpp
 	static int HowMany() {return num_string;}
 	int count = String::HowMany();
```

###20. 通过char*创建string

```cpp
 	char s[] = {'a', 'b', 'c'};
 	string* test1 = new string(&s[1]);
```

###21. 重载<<运算符
 
```cpp
 	friend ostream& operator<<(ostream& os, const Stonewt& obj);
 	ostream& operator<<(ostream& os, const Stonewt& obj)
	{
	    os<<obj.stone<<endl;
	    return os;
	}
```

###22. 类的静态变量

```cpp
	static int count;
	int Stonewt::count = 0;
```

###23. 使用explicit，让编译器不强转类型

```cpp
	Class Student
	{
		explicit Student(int n) {}
	};
	Sutdent doh("test", 10);
	doh = 5;
```

C++提供了关键字`explicit`，可以阻止不应该允许的经过转换构造函数进行的隐式转换的发生。声明为explicit的构造函数不能在隐式转换中使用。

###24. virtual public继承，为解决菱形集成问题

###25. 泛型编程

```cpp
	bool Stack::push(const Item& item)
	{}
```

应改为
	
```cpp
	template<class Type>
	bool Stack<Type>::push(const TYpe& item)
	{}
```

###26. 模板别名

```cpp
	template<typename T>
	using arrtype = std::array<T, 12>
```

###27. try block

```cpp
	try {
        z = hmean(x, y);
    } catch (const char* s) {
        cout<<s<<endl;
        cout<<"enter new two number: ";
        continue;
    }
    throw "bad hmean() arguments a== -b";
```

###28. 未捕获异常不会导致程序立刻异常终止。

相反，程序将首先调用函数terminate（）。在默认情况下， terminate（）调用abort（）函数，可以指定terminate（）应调用的函数（而不是abort（））来修改terminate（）的这种行为。为此，可调用set_terminate()函数。set_terminate（）和terminate（）都是在头文件exception中声明的。

```cpp
	void myQuit()
	{
	    cout<<"Terminating due to uncaught exception!";
	    exit(5);
	}
	set_terminate(myQuit);
```

###29. RTTI (Runtime Type Identification)工作原理

1. 如果可能的话， dynamic_cast运算符将使用一个指向基类的指针来生成一个指向派生类的指针；否则， 该运算符返回0——空指针
2. typeid运算符返回一个指出对象的类型的值
3. type_info结构存储了有关特定类型的信息。

###30. dynamic_cast<>

```cpp
	Worker* wk = new Waiter();
    Singer* sg = dynamic_cast<Singer*>(wk);	// null
    Waiter* wt = dynamic_cast<Waiter*>(wk);	// not null
```

###31. typeid, type_info

```cpp
	cout<<"name = "<<typeid(Worker).name()<<", id = "<<typeid(Worker).hash_code()<<endl;
```

###32. dynamic_cast ：使得在类层次结构中进行向上转换	dynamic_cast<type_name>()

```cpp
	const_cast ：用于执行只有一种用途的类型转换，即改变值为const 或volatile，	const_cast<type_name>()
```

###33. 智能指针

```cpp
	{
        auto_ptr<Report> ps(new Report("using auto_ptr"));
        ps->comment();
    }
    
    {
        shared_ptr<Report> ps(new Report("using share_ptr"));
        ps->comment();
    }
    
    {
        unique_ptr<Report> ps(new Report("using unique_ptr"));
        ps->comment();
    }
```

###34. 问题:会删除ps

```cpp
	auto_ptr<string> ps(new string("t"));
	auto_ptr<string> vocation;
	vacation = ps;
```

解决方案：
1. 定义复制运算符，是指执行深复制
2. 简历所有权概念，对于特定的对象，只能有一个智能指针可拥有它， 这样只有拥有对象的智能指针的构造函数会删除该对象。然后，让复制操作转让所有权。这就是用于auto_ptr和unique_ptr的策略， 但unique_ptr的策略更严格。
	
```cpp
		auto_ptr<Report> ps(new Report("using auto_ptr"));
        auto_ptr<Report> ps1 = ps;
        ps->comment();	// ps = NULL
```

3. 创建智能更高的指针，跟踪引用特定对象的智能指针数。这称为引用计数。仅当最后一个指针过期时，才调用delete。share_ptr

###35. Lambda函数
	
`[](int x) {return x % 3 == 0;}	或 [](int x) -> double {return x % 3 == 0;}`，类似 `bool f(int x) {return x % 3 == 0;}`
	
```cpp
	auto mode3 = [](int x) {return x % 3 == 0;}
	count 3 = std::count_if(numbers.begin(), numbers.end(), mode3);
```

###36. static_assert

```cpp
#define assert_static(e)    \
    do{   \
        enum {assert_static__ = 1/(e)};\
    }while(0)
template <typename T, typename U>
void bit_copy(T& a, U& b)
{
//    assert_static(sizeof(a) == sizeof(b));
    static_assert(sizeof(a) == sizeof(b), "error");//此处会报错
    memcpy(&a, &b, sizeof(a));
}

int main()
{
	int a = 0x2468;
    double b;
    bit_copy(a, b);
    return 1;
}

```
