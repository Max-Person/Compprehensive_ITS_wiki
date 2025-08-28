[its_QuestionGen](https://github.com/Max-Person/its_QuestionGen)  - компонент системы, служащий для построения структуры наводящих вопросов на основе деревьев решений, а также для реализации текстового взаимодействия с пользователем на основе этой структуры
## Функционал в этом модуле
- Построение структуры (последовательностей) наводящих вопросов на основе [[Дерево (граф) решений|графа мыслительных процессов]].
- Генерация текстовых формулировок наводящих вопросов (а также ответов и объяснений для них) для данной структуры в конкретной ситуации.
	- Введение [[Выражения|выражений]] в стороннюю систему текстовых шаблонов (см. [JavaStringTemplating](https://github.com/Max-Person/JavaStringTemplating)) для построения формулировок на основе данных о предметной области.
	- Динамическое построение формулировок на основе структуры [[Выражения|выражений]] в конкретных узлах ГМП.

Подробнее о функционале этого модуля читайте в других статьях данного раздела.
## Примеры использования
Примеры использования описаны на Java, т.к. я думаю, что вы с большей вероятностью будете использовать именно ее (использование на Kotlin в принципе аналогично, и более просто).

Данные примеры также полагаются на код из its_DomainModel, подробнее см. [[Об its_DomainModel#Примеры использования|их примеры использования]].
#### Построение автомата наводящих вопросов
```java  
DomainSolvingModel model = ... ;
    
QuestionAutomata questionAutomata = FullBranchStrategy.INSTANCE.buildAndFinalize(  
    model.getDecisionTree().getMainBranch(),  
    new EndQuestionState()  
);
```
#### Построение диалоговой ситуации
```java
DomainModel situationModel = ... ;

String localizationCode = "RU";
QuestioningSituation questioningSituation = new QuestioningSituation(situationModel, localizationCode)
```
#### Ведение диалога в конкретной ситуации
```java
QuestionAutomata questionAutomata = ... ;
QuestioningSituation = ... ;

QuestionState currentState = questionAutomata.getInitState();  
while (currentState != null) {  
    QuestionStateResult stateResult = currentState.getQuestion(questioningSituation);  
    //Если переход к следующему вопросу  
    if(stateResult instanceof QuestionStateChange stateChange){  
        //<Как-то обрабатываем объяснение о переходе к след. вопросу>  
        handleExplanation(stateChange.getExplanation());  
        currentState = stateChange.getNextState();  
    }  
    //Иначе если вопрос  
    else if (stateResult instanceof Question question) {  
        //<Как-то получаем ответы пользователя на вопрос>  
        //например, question.ask()List<Integer> answers = handleQuestion(question);  
        QuestionStateChange stateChange = currentState.proceedWithAnswer(questioningSituation, answers);  
        //<Как-то обрабатываем объяснение о переходе к след. вопросу>  
        handleExplanation(stateChange.getExplanation());  
        currentState = stateChange.getNextState();  
    }  
}
```



