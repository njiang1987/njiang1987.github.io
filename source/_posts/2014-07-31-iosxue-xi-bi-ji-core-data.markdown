---
layout: post
title: "iOS学习笔记——Core Data"
date: 2014-07-31 23:57:17 +0800
comments: true
categories: 技术
tags: iOS
---
##7.1. 什么是Core Data

Core Data是一个Cocoa框架，用于为管理对象图提供基础实现，以及为多种文件格式的持久化提供支持。管理对象图包含的工作如撤销（undo）和重做（redo）、有效性检查、以及保证对象关系的完整性等。对象的持久化意味着Core Data可以将模型对象保存到持久化存储中，并在需要的时候将它们取出。Core Data应用程序的持久化存储（也就是对象数据的最终归档形式）的范围可以从XML文件到SQL数据库。Core Data用在关系数据库的前端应用程序是很理想的，但是所有的Cocoa应用程序都可以利用它的能力。

Core Data的核心概念是托管对象。托管对象是由Core Data管理的简单模型对象，但必须是NSManagedObject类或其子类的实例。可以用一个称为托管对象模型的结构（schema）来描述Core Data应用程序的托管对象（Xcode中包含一个数据建模工具，可以帮助您创建这些结构）。托管对象模型包含一些应用程序托管对象（也称为实体）的描述。每个描述负责指定一个实体的属性、它与其它实体的关系、以及像实体名称和实体表示类这样的元数据。

在一个运行着的Core Data程序中，有一个称为托管对象上下文的对象负责管理托管对象图。图中所有的托管对象都需要通过托管对象上下文来注册。该上下文对象允许在图中加入或删除对象，以及跟踪图中对象的变化，并因此可以提供撤销（undo）和重做（redo）的支持。当准备好保存对托管对象所做的修改时，托管对象上下文负责确保那些对象处于正确的状态。当Core Data应用程序希望从外部的数据存储中取出数据时，就向托管对象上下文发出一个取出请求，也就是一个指定一组条件的对象。在自动注册之后，上下文对象会从存储中返回与请求相匹配的对象。

托管对象上下文还作为访问潜在Core Data对象集合的网关，这个集合称为持久化堆栈。持久化堆栈处于应用程序对象和外部数据存储之间，由两种不同类型的对象组成，即持久化存储和持久化存储协调器对象。持久化存储位于栈的底部，负责外部存储（比如XML文件）的数据和托管对象上下文的相应对象之间的映射，但是它们不直接和托管对象上下文进行交互。在栈的持久化存储上面是持久化存储协调器，这种对象为一或多个托管对象上下文提供一个访问接口，使其下层的多个持久化存储可以表现为单一一个聚合存储。图7-1显示了Core Data架构中各种对象之间的关系。

{% img center /uploads/2014-07-31/1.png 370 396 %} 

图7-1

Core Data中包含一个NSPersistentDocument类，它是NSDocument的子类，用与协助Core Data和文档架构之间的集成。持久化文档对象创建自己的持久化堆栈和托管对象上下文，将文档映射到一个外部的数据存储；NSPersistentDocument对象则为NSDocument中读写文档数据的方法提供缺省的实现。

通过Core Data管理应用程序的数据模型，可以极大程度减少需编写的代码数量。Core Data还具有下述特征：

1. 将对象数据存储在SQLite数据库以获得性能优化。
2. 提供NSFetchedResultsController 类用于管理表视图的数据。即将Core Data的持久化存储显示在表视图中，并对这些数据进行管理：增、删，改。
3. 管理undo/redo操作。
4. 检查托管对象的属性值是否正确。

###7.1.1. Core Data基本架构

在大多数应用中，需要打开一个文件，此文件包含一个有多个对象的归档，或者包含一个对至少一个根对象的引用。还需要能够归档所有对象到一个文件，并跟踪对象的变化。例如，在一个员工管理应用中，需要一种方法来打开一个文件，其中包含员工和部门对象的归档，并包含一个对至少一个根对象的引用——例如，含有全体员工的数组——如图7-2。还需要能够归档所有员工和所有部门到一个文件。

{% img center /uploads/2014-07-31/2.png 456 455 %} 

图 7-2

使用的Core Data框架，大多数功能可以自动提供，这主要通过名为托管对象上下文（managed object context，或只是“上下文”，类NSManagedObjectContext的实例）来实现。托管对象的上下文就像一个网关，通过它可以访问底层的框架对象集合——这些对象集合统称为持久化堆栈（persistence stack）——它在应用程序和外部数据存储的对象之间提供访问通道。在堆栈的底部是持久化对象存储（persistent object stores），如图7-3所示。

{% img center /uploads/2014-07-31/3.png 510 472 %} 

图7-3

Core Data不局限于基于文档的应用程序，也能创建基于Core Data的无用户界面的Utility应用。当然其他应用程序也能使用Core Data的。

####7.1.1.1. 托管对象和上下文(Managed Objects and Contexts)

可以把托管对象上下文作为一个智能便笺。当从持久化存储中获取对象时，这些对象的临时副本会在便笺上形成一个对象图（或者对象图的集合。对象图即对象 + 对象之间的联系），然后便可以任意修改这些对象。除非保存这些修改，否则持久化存储是不会受影响的。

Core Data框架中的模型对象（Model Objects，它是一种含有应用程序数据的对象类型，提供对数据的访问并实现逻辑来处理数据）称为托管对象。所有托管对象都必须通过托管对象上下文进行注册。该上下文对象允许在图中加入或删除对象，以及跟踪图中对象的变化，并因此可以提供撤销（undo）和重做（redo）的支持。当准备好保存对托管对象所做的修改时，托管对象上下文负责确保那些对象处于正确的状态。

如果要保存所做的更改，上下文首先要验证对象是有效的。如果对象有效，所作的更改会被写到持久化存储中，创建对象会添加新记录，删除对象则会删除记录。

可以在应用程序中使用多个上下文。对于持久化存储中的每一个对象，只有唯一的一个托管对象和给定的上下文相关联。从不同的角度考虑，持久化存储中的一个给定的对象，可在多个上下文中同时被编辑。然而，每个上下文都有它自己的对应着源对象的托管对象，每个托管对象都单独编辑。这样保存时就会导致数据不一致。Core Data提供了一些方法来处理这个问题，比如使用- (void)refreshObject:(NSManagedObject *)object mergeChanges: (BOOL)flag方法从持久化存储中获取最新的值来更新托管对象的持久化属性。

####7.1.1.2.获取数据请求（Fetch Requests）

使用托管对象上下文来检索数据时，会创建一个获取请求（fetch request，类NSFetchRequest的实例）的所有员工，按照工资最高到最低排序”。获取请求由三部分组成。最简单的获取请求必须指定一个实体的名称（这就暗示每次只能取一种实体类型）。获取请求也可能包含一个谓词对象，指定对象必须符合的条件（比如“市场部的所有员工”）。获取请求还包含一个排序描述方式对象的数组，指定对象应该出现的顺序（比如“按照工资最高到最低排序”），如图7-4所示。

{% img center /uploads/2014-07-31/4.png 487 285 %} 

图 7-4

发送获取请求给托管对象上下文，它从与持久化存储相关联的数据源中返回的匹配请求的对象（也可能没有返回）。由于所有托管对象必须在托管对象上下文中注册，从获取请求返回的对象自动注册在用来获取的上下文中。上面说到，对于持久化存储中的每一个对象，只有唯一的一个托管对象和给定的上下文相关联。如果上下文中已经包含了一个托管对象作为获取请求返回的对象，那么这个托管对象则作为获取请求结果返回。

Core Data框架试图尽可能的高效。Core Data是需求驱动的，因此它只会创建实际需要的对象，不会额外创建更多对象。对象图并不代表持久化存储中的所有对象。仅指定一个持久化存储并不会把任何数据对象注册到托管对象上下文中。当从持久化存储中获取对象的一个​​子集，只能得到请求的对象。如果不再需要一个对象，默认情况下它会被释放。（这当然与从对象图中删除对象不一样。）

####7.1.1.3.持久化存储协调器

如上所述，在应用程序和外部数据存储的对象之间提供访问通道的框架对象集合统称为持久化堆栈（persistence stack）。在堆栈顶部的是托管对象上下文下，在堆栈底部的是持久化对象存储（persistent object stores）。在托管对象上下文和持久化对象存储之间便是持久化存储协调器（persistent store coordinator）。应用程序通过类NSPersistentStoreCoordinator的实例访问持久化对象存储。

持久化存储协调器为一或多个托管对象上下文提供一个访问接口，使其下层的多个持久化存储可以表现为单一一个聚合存储。一个托管对象上下文可以基于持久化存储协调器下的所有数据存储来创建一个对象图。持久化存储协调器只能与一个托管对象模型相关联。如果想把不同的实体放到不同存储中，必须依据托管对象模型中定义的配置把模型实体分区（partition）。

图7-5显示了一个例子，把员工和部门存储在一个文件中，并把客户和公司存储在另一个文件中。当获取对象时，他们会自动从相应的文件中返回；当保存更改时，会自动归档到相应的文件。

{% img center /uploads/2014-07-31/5.png 370 396 %} 

图 7-5

####7.1.1.4.持久化存储（Persistent Stores）

一个特定的持久化对象存储是与单个文件或其他外部数​​据存储相关联的，负责存储中的数据和托管对象上下文中的对象之间的映射。通常情况下，读者与持久化对象存储之间只有一个交互，就是在应用程序中为一个新的外部数据存储指定位置（例如，当用户打开或保存文档）。Core Data的大多数交互则通过托管对象上下文实现。

应用程序代码中——特别是应用程序中托管对象的相关逻辑——不应该为持久化存储中的数据存储作出任何假设（即由Core Data自行处理）。Core Data为几种文件格式提供原生支持，选择使用哪一个取决于应用程序的需求。应用程序体系架构保持不变，也应该能在应用程序的某个阶段，选择一个不同的文件格式。此外，如果应用程序经过适当的抽象，那么不增加任何操作，就能够利用框架的后续增强功能。例如——即使在刚开始时，只能从本地文件系统获取数据——如果一个应用程序没有假设从哪里获取数据，同时后面的某个阶段又想为一种新的远程持久化存储类型添加支持，它也应该能够使用这种新类型而不用修改代码。

知识点

尽管Core Data虽然支持的SQLite作为其持久化存储类型之一，Core Data也无法管理任意的SQLite数据库。要使用SQLite数据库，Core Data必须自行创建和管理数据库。

####7.1.1.5.持久化文件（Persistent Documents）

可以通过程序创建和配置持久化堆栈。然而，在许多情况下，只是想创建一个基于文档的应用程序来读写文件。使用类NSDocument的子类NSPersistentDocument，便可轻松的利用Core Data完成此事。默认情况下，NSPersistentDocument实例便已经创建了自己的即用型持久化堆栈，包括一个托管对象上下文，和单个持久化对象存储。在这种情况下，有文档和外部数据存储之间便建立起一个“一对一”映射。

NSPersistentDocument类提供了方法来访问文档的托管对象上下文，并提供NSDocument方法的标准实现来读写文件，这些操作都是在Core Data框架内进行的。默认情况下，不必编写任何额外的代码来处理对象的持久化。一个持久化文档的撤消（undo）功能也被集成在托管对象上下文。

###7.1.2.托管对象（Managed Objects）和托管对象模型（Managed Object Model）

为了既管理的对象图，也支持对象持久化，Core Data需要对它操作的对象进行详尽的描述。托管对象模型（managed object model）是一个结构（schema），用来描述应用程序中的托管对象，或实体，如图7-6所示。通常使用Xcode的数据模型设计工具来创建托管对象模型。（也可以在运行时使用代码来建模。）它是类NSManagedObjectModel的一个实例。

{% img center /uploads/2014-07-31/6.png 368 136 %} 

图 7-6

该模型由一个实体描述对象（类NSEntityDescription实例）的集合组成，每个对象提供一个实体的元数据（metadata），包括实体名，实体在应用程序中的类名（类名不必要与实体名称一样），实体的属性和实体之间关系。实体的属性和关系依次由属性和关系描述对象表示出来，如图7-7所示。

{% img center /uploads/2014-07-31/7.png 442 352 %}  

图 7-7

托管对象必须是NSManagedObject或者NSManagedObject子类的任一实例。NSManagedObject能够表述任何实体。它使用一个私有的内部存储，以维护其属性，并实现托管对象所需的所有基本行为。托管对象有一个指向实体描述的引用。实体描述表述了实体的元数据，包括实体的名称，实体的属性和实体之间的关系。可以创建NSManagedObject子类来实现实体的其他行为。

###7.1.3.基本实现
1. 指定存储数据文件

```objc
NSArray *paths = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES);
NSString *documentsDirectory = [paths lastObject];
NSString *persistentStorePath = [[documentsDirectory stringByAppendingPathComponent:@"TopSongs.sqlite"] retain];
```

2. 创建托管对象模型

```objc
NSManagedObjectModel  *managedObjectModel = [[NSManagedObjectModel mergedModelFromBundles:nil] retain];
```

3. 创建持久化存储协调器，并使用SQLite数据库做持久化存储

```objc
NSURL *storeUrl = [NSURL fileURLWithPath:self.persistentStorePath];
NSPersistentStoreCoordinator *persistentStoreCoordinator = [[NSPersistentStoreCoordinator alloc] initWithManagedObjectModel:self.managedObjectModel];
NSError *error = nil;
NSPersistentStore *persistentStore = [persistentStoreCoordinator addPersistentStoreWithType:NSSQLiteStoreType configuration:nil URL:storeUrl options:nil error:&amp;error];
```

4. 创建托管对象上下文

```objc
 NSManagedObjectContext *managedObjectContext = [[NSManagedObjectContext alloc] init];
[managedObjectContext setPersistentStoreCoordinator: self.persistentStoreCoordinator];
```

5. 创建实体描述对象

```objc
 NSEntityDescription *entityDescription = [[NSEntityDescription entityForName:@"Song" inManagedObjectContext: self.managedObjectContext] retain];
```

6. 创建托管对象

```objc
 NSManagedObject *managedObject = [[NSManagedObject alloc] initWithEntity:self.entityDescription insertIntoManagedObjectContext:self.managedObjectContext];
```

7. 保存

```objc
 NSError *saveError = nil;
[self.managedObjectContext save:&amp;saveError]
```

8. 创建获取数据请求

```objc
 NSFetchRequest *fetchRequest = [[NSFetchRequest alloc] init];
// 数据排序，Sort key为NSManagedObject托管对象的一个属性
NSSortDescriptor *sortDescriptor = [[NSSortDescriptor alloc] initWithKey:@"" ascending:YES];
NSArray *sortDescriptors = [[NSArray alloc] initWithObjects:sortDescriptor, nil];
[fetchRequest setSortDescriptors:sortDescriptors];
```

9. 获取持久化存储中的数据，并对数据进行缓存

```objc
 NSFetchedResultsController *fetchedResultsController = [[NSFetchedResultsController alloc]
        initWithFetchRequest:self.fetchRequest
        managedObjectContext:self.managedObjectContext
        sectionNameKeyPath:nil
        cacheName:@""];
 
NSError *error;
BOOL success = [self.fetchedResultsController performFetch:&amp;error];
```

10. 将数据显示在UITableView中

```objc
- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView {
    return [[self.fetchedResultsController sections] count];
}
- (NSInteger)tableView:(UITableView *)table numberOfRowsInSection:(NSInteger)section {
    id  sectionInfo = [[self.fetchedResultsController sections] objectAtIndex:section];
    return [sectionInfo numberOfObjects];
}
- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    UITableViewCell *cell = ;
    NSManagedObject *managedObject = [self.fetchedResultsController objectAtIndexPath:indexPath];
    // Configure the cell with data from the managed object.
    return cell;
}
 
- (NSString *)tableView:(UITableView *)tableView titleForHeaderInSection:(NSInteger)section {
    id  sectionInfo = [[self.fetchedResultsController sections] objectAtIndex:section];
    return [sectionInfo name];
}
- (NSArray *)sectionIndexTitlesForTableView:(UITableView *)tableView {
    return [self.fetchedResultsController sectionIndexTitles];
}
- (NSInteger)tableView:(UITableView *)tableView sectionForSectionIndexTitle:(NSString *)title atIndex:(NSInteger)index {
    return [self.fetchedResultsController sectionForSectionIndexTitle:title atIndex:index];
}
```

转自:<http://hxsdit.com/1622>