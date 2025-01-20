its_DomainModel это проект, служащий основой для остальных проектов its_\*, и отвечающий за создание и хранение необходимых моделей данных о предметной области.

**Проекты its_\* включают в себя:**
- its_DomainModel (этот проект) - создание, валидация и преобразование моделей данных (модели данных о конкретных задачах, а также модели деревьев решений, решающих эти задачи)
- [its_Reasoner](https://github.com/Max-Person/its_Reasoner) - вычисления (reasoning) на основе деревьев решений
- [its_QuestionGen](https://github.com/Max-Person/its_QuestionGen) - создание наводящих вопросов на основе деревьев решений, текстовое взаимодействие с пользователем

Данные проекты задуманы для использования в качестве **библиотек** в других проектах, написанных на Java или Kotlin (подробнее про языки [[#Java и Kotlin|ниже]]), т.е. сами не несут исполняемого кода как такового.
**Подробнее о функционале, предоставляемом данной библиотекой, читайте в остальных частях вики** (содержание можно видеть справа).

Ниже - о том, как начать использовать данный проект.
## Установка как зависимости

Как автор данных проектов, **я рекомендую использовать Maven + [JitPack](https://jitpack.io/)  для подключения проектов its_\* как зависимостей в ваших собственных проектах**.
Для этого необходимо:
1\. В pom.xml своего проекта указать репозиторий JitPack:
```xml
<repositories>
	<repository>
		<id>jitpack.io</id>
		<url>https://jitpack.io</url>
	</repository>
</repositories>
```
2\. Также в pom.xml указать данный проект как зависимость:
```xml
<dependency>
	<groupId>com.github.Max-Person</groupId>
	<artifactId>its_DomainModel</artifactId>
	<version>...</version>
</dependency>
```
В качестве версии JitPack может принимать название ветки, тег (release tag), или хэш коммита. Для данных проектов я рекомендую указывать либо `master-SNAPSHOT` для получения самых последних изменений с master-ветки, либо хэш конкретного коммита (например самого нового), чтобы ваш проект не сломался с обновлением библиотеки.

3\. В IntelliJ IDEA надо обновить зависимости Maven (Maven -> Reload All Maven Projects), и все, данный проект настроен для использования в качестве библиотеки.
> [!note]
Обратите внимание, что JitPack собирает нужные артефакты только по запросу - т.е. когда вы подтягиваете зависимость. Это значит, что первое подобное подтягивание скорее всего займет несколько минут - JitPack-у нужно будет время на билд.
После завершения такого долгого билда, в IDEA может отобразиться надпись "Couldn't aqcuire locks", как будто произошла ошибка - в этом случае просто обновитесь еще раз, это будет быстро.

4\. Вместе с артефактами данной библиотеки всегда доступен ее исходный код, а в нем и документация (kotlindoc/javadoc). **Проект на 90% задокументирован, поэтому смотрите на документацию к используемым вами методам!** 
Для того, чтобы исходный код и документация тоже подтянулись, нужно в IntelliJ IDEA сделать Maven -> Download Sources and/or Documentation -> Download Sources and Documentation
### Альтернативные варианты установки

JitPack позволяет использовать GitHub-репозитории в качестве Maven-артефактов, а т.е. позволяет подтягивать Maven-зависимости прямо из репозиториев. **Это кажется самым простым способом использовать данный проект.**

Тем не менее, если вы хотите иметь больше контроля над проектом (например если вы ~~сошли с ума~~ хотите поменять в нем какую-то логику), вы можете **собрать его самостоятельно**:
1. Склонируйте данный репозиторий
2. Запустите установку `mvn install` 
   (в IntelliJ IDEA: Maven ->DomainModel -> Lifecycle -> install)
3. После установки проект появится как артефакт (соответствующий указанным в pom.xml данным) в вашем локальном Maven-репозитории (.m2)
4. Укажите в вашем проекте соответствующую зависимость.
## С чего начать

Здесь и ниже в этом разделе - различные обособленные примеры использования данного проекта. Описаны на Java, т.к. я думаю, что вы с большей вероятностью будете использовать именно ее (использование на Kotlin в принципе аналогично, и более просто)
#### Создание модели предметной области

Создать [[Модель предметной области|модель предметной области]] из [[LOQI|.loqi]] файла:
```java
DomainModel domainModel = DomainLoqiBuilder.buildDomain(new FileReader(filename)); 
```

Создать модель предметной области из папки с [[Словари + RDF|.csv словарями и RDF файлами]]:
```java
DomainModel domainModel = DomainDictionariesRDFBuilder.buildDomain(  
    directoryPath,  
    Collections.emptySet() 
);
```

#### Дополнение модели предметной области новыми данными

Наполнить существующую модель данными из  .loqi файла:
```java
domainModel.addMerge(DomainLoqiBuilder.buildDomain(new FileReader(newFilename)))
```

Наполнить существующую модель данными из RDF:
```java
DomainRDFFiller.fillDomain(  
    domainModel,  
    ttlFilePath,  //путь к .ttl файлу с RDF
    Collections.emptySet(), //или Set.of(DomainRDFFiller.Option.NARY_RELATIONSHIPS_OLD_COMPAT)  
    someTtlBasePrefix //префикс, использующийся в .ttl файле - например RDFUtils.POAS_PREF  
);
```

#### Запись модели предметной области в файл

Запись в виде LOQI:
```java
DomainLoqiWriter.saveDomain(  
    domainModel,  
    new FileWriter(filename),  
    Collections.emptySet()  
);
```

Запись в виде RDF:
```java
DomainRDFWriter.saveDomain(  
    domainModel,  
    new FileWriter(filename),  
    someTtlBasePrefix, //префикс, использующийся в .ttl файле - например RDFUtils.POAS_PREF    
    Collections.emptySet() //или Set.of(DomainRDFWriter.Option.NARY_RELATIONSHIPS_OLD_COMPAT)  
);
```

#### Создание дерева решений

Построение [[Дерево (граф) решений|дерева решений]] из .xml файла
```java
DecisionTree decisionTree = DecisionTreeXMLBuilder.fromXMLFile(filename);
```

### Типичный пример использования моделей

```java
//Строим и валидируем составную модель (предметная область + теги + деревья решений)  
DomainSolvingModel domainSolvingModel = new DomainSolvingModel(  
    directoryPath,  
    DomainSolvingModel.BuildMethod.LOQI  
);  
domainSolvingModel.validate();  
  
//Получаем общую модель для под-области  
DomainModel subDomainModel = domainSolvingModel.getMergedTagDomain(someTagName);  
  
//Получаем модель для конкретной ситуации  
DomainModel situationDomain = DomainLoqiBuilder.buildDomain(new FileReader(situationFileName));  
//Объединяем модель ситуации с моделью под-области - делаем ее полной  
situationDomain.addMerge(subDomainModel);  
//Валидируем модель ситуации  
situationDomain.validateAndThrow();  
  
//Получаем дерево решений из составной модели  
DecisionTree decisionTree = domainSolvingModel.getDecisionTree();  
  
//...проводим дальнейшие вычисления (см. its_Reasoner)
```
## Java и Kotlin

Здесь вкратце о том, почему здесь все написано на Kotlin, и что с этим делать.

Kotlin выбран для проекта без особых на то причин - когда он только начинался, мы посчитали что это будет хорошей возможностью познакомиться с новым языком. В принципе, об этом решении мы не пожалели - это оказался действительно интересный и приятный язык.

При этом, Kotlin компилируется под JVM, а значит, [может быть вызван из Java-кода](https://kotlinlang.org/docs/java-to-kotlin-interop.html). Это значит, что использование данных библиотек возможно из ваших Java-проектов, если вам комфортнее использовать знакомую джаву, чем неизвестный котлин (что, в принципе, понимаемо).
При подобном использовании могут возникать некоторые заминки и различия (например в том, как называются параметры методов, и как они передаются), но существенных проблем в таком подходе нет.