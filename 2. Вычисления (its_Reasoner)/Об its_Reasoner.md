[its_Reasoner](https://github.com/Max-Person/its_Reasoner) - модуль системы, служащий для реализации вычислений по [[Дерево (граф) решений|графам мыслительных процессов]], построенных с помощью [[Об its_DomainModel|its_DomainModel]]
## Функционал в этом модуле
- Реализация вычислений [[Выражения|LOQI-выражений]].
- Реализация выполнения логики [[Дерево (граф) решений|графов мыслительных процессов]].
	- В т.ч. предоставление информации о пройденном пути в графе.

Подробнее о функционале этого модуля читайте в других статьях данного раздела.
## Примеры использования
Примеры использования описаны на Java, т.к. я думаю, что вы с большей вероятностью будете использовать именно ее (использование на Kotlin в принципе аналогично, и более просто).

Данные примеры также полагаются на код из its_DomainModel, подробнее см. [[Об its_DomainModel#Примеры использования|их примеры использования]].
#### Создание учебной ситуации
```java
DomainModel situationModel = ...  ;
  
LearningSituation situation = new LearningSituation(  
    situationModel,  
    LearningSituation.collectDecisionTreeVariables(situationModel)   //мапа переменных дерева решений
);
```
#### Вычисление LOQI-выражения
```java
Operator expr = ... ;
LearningSituation situation = ... ;
    
Object result = expr.use(new DomainInterpreterReasoner(  
    situation,  
    new HashMap<>() //пустая мапа контекстных переменных  
));
```
#### Выполнений действий графа мыслительных процессов
```java
DomainSolvingModel model = ... ;
LearningSituation situation = ... ;
  
DecisionTreeTrace decisionTreeTrace = DecisionTreeReasoner.solve(  
    model.getDecisionTree(),  
    situation  
);
```


