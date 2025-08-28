 [its_DomainModel](https://github.com/Max-Person/its_DomainModel)  - модуль, служащий основой для остальных модулей Compprehensive ITS (its_\*), и отвечающий за создание и хранение необходимых моделей данных о предметной области.
## Функционал в этом модуле
- Построение [[Модель предметной области|модели предметной области]] - описание сущностей и их типов, присущих данной предметной области.
- Построение [[Выражения|LOQI-выражений]], описывающих действия и рассуждения над моделью предметной области.
- Построение [[Дерево (граф) решений|графов мыслительных процессов]], представляющих модель мышления, необходимого для решения некоторой задачи в заданной предметной области.
- Валидация описанных выше моделей.

Подробнее о функционале этого модуля читайте в других статьях данного раздела.
## Примеры использования
Примеры использования описаны на Java, т.к. я думаю, что вы с большей вероятностью будете использовать именно ее (использование на Kotlin в принципе аналогично, и более просто).
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