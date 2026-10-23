<!-- i18n-source: 03-skills/refactor/references/refactoring-catalog.md -->
<!-- i18n-source-sha: b9a973b -->
<!-- i18n-date: 2026-10-23 -->

# Каталог рефакторингов

Подобранный каталог приёмов рефакторинга из книги Мартина Фаулера (Martin Fowler) *Refactoring* («Рефакторинг», 2-е издание). У каждого рефакторинга есть мотивация, пошаговая механика и примеры.

> «Рефакторинг определяется его механикой — точной последовательностью шагов, по которой вы проводите изменение.» — Martin Fowler

---

## Как пользоваться этим каталогом

1. **Опознайте запах** по справочнику запахов кода
2. **Найдите подходящий рефакторинг** в этом каталоге
3. **Следуйте механике** шаг за шагом
4. **Тестируйте после каждого шага**, чтобы поведение сохранилось

**Золотое правило**: если какой-то шаг занимает больше 10 минут, разбейте его на меньшие шаги.

---

## Самые частые рефакторинги

### Извлечение метода (Extract Method)

**Когда применять**: длинный метод, дублирующийся код, нужно дать имя понятию

**Мотивация**: превратить фрагмент кода в метод, имя которого объясняет назначение.

**Механика**:
1. Создайте новый метод с именем по тому, что он делает (а не как)
2. Скопируйте фрагмент кода в новый метод
3. Найдите локальные переменные, которые используются во фрагменте
4. Передайте локальные переменные параметрами (или объявите их в методе)
5. Корректно обработайте возвращаемые значения
6. Замените исходный фрагмент вызовом нового метода
7. Протестируйте

**До**:
```javascript
function printOwing(invoice) {
  let outstanding = 0;

  console.log("***********************");
  console.log("**** Customer Owes ****");
  console.log("***********************");

  // Вычислить задолженность
  for (const order of invoice.orders) {
    outstanding += order.amount;
  }

  // Напечатать подробности
  console.log(`name: ${invoice.customer}`);
  console.log(`amount: ${outstanding}`);
}
```

**После**:
```javascript
function printOwing(invoice) {
  printBanner();
  const outstanding = calculateOutstanding(invoice);
  printDetails(invoice, outstanding);
}

function printBanner() {
  console.log("***********************");
  console.log("**** Customer Owes ****");
  console.log("***********************");
}

function calculateOutstanding(invoice) {
  return invoice.orders.reduce((sum, order) => sum + order.amount, 0);
}

function printDetails(invoice, outstanding) {
  console.log(`name: ${invoice.customer}`);
  console.log(`amount: ${outstanding}`);
}
```

---

### Встраивание метода (Inline Method)

**Когда применять**: тело метода столь же ясно, как его имя; избыточное делегирование

**Мотивация**: убрать ненужную косвенность, когда метод не добавляет пользы.

**Механика**:
1. Проверьте, что метод не полиморфный
2. Найдите все вызовы метода
3. Замените каждый вызов телом метода
4. Тестируйте после каждой замены
5. Удалите определение метода

**До**:
```javascript
function getRating(driver) {
  return moreThanFiveLateDeliveries(driver) ? 2 : 1;
}

function moreThanFiveLateDeliveries(driver) {
  return driver.numberOfLateDeliveries > 5;
}
```

**После**:
```javascript
function getRating(driver) {
  return driver.numberOfLateDeliveries > 5 ? 2 : 1;
}
```

---

### Извлечение переменной (Extract Variable)

**Когда применять**: сложное выражение, которое трудно понять

**Мотивация**: дать имя части сложного выражения.

**Механика**:
1. Убедитесь, что у выражения нет побочных эффектов
2. Объявите неизменяемую переменную
3. Присвойте ей результат выражения (или его части)
4. Замените исходное выражение переменной
5. Протестируйте

**До**:
```javascript
return order.quantity * order.itemPrice -
  Math.max(0, order.quantity - 500) * order.itemPrice * 0.05 +
  Math.min(order.quantity * order.itemPrice * 0.1, 100);
```

**После**:
```javascript
const basePrice = order.quantity * order.itemPrice;
const quantityDiscount = Math.max(0, order.quantity - 500) * order.itemPrice * 0.05;
const shipping = Math.min(basePrice * 0.1, 100);
return basePrice - quantityDiscount + shipping;
```

---

### Встраивание переменной (Inline Variable)

**Когда применять**: имя переменной не сообщает больше, чем само выражение

**Мотивация**: убрать ненужную косвенность.

**Механика**:
1. Проверьте, что у правой части нет побочных эффектов
2. Если переменная не неизменяемая, сделайте её такой и протестируйте
3. Найдите первое обращение и замените его выражением
4. Протестируйте
5. Повторите для всех обращений
6. Удалите объявление и присваивание
7. Протестируйте

---

### Переименование переменной (Rename Variable)

**Когда применять**: имя неясно сообщает о назначении

**Мотивация**: хорошие имена критичны для чистого кода.

**Механика**:
1. Если переменная широко используется, подумайте об инкапсуляции
2. Найдите все обращения
3. Измените каждое обращение
4. Протестируйте

**Советы**:
- Используйте имена, раскрывающие намерение
- Избегайте сокращений
- Используйте терминологию предметной области

```javascript
// Плохо
const d = 30;
const x = users.filter(u => u.a);

// Хорошо
const daysSinceLastLogin = 30;
const activeUsers = users.filter(user => user.isActive);
```

---

### Изменение объявления функции (Change Function Declaration)

**Когда применять**: имя функции не объясняет назначение, параметры нужно изменить

**Мотивация**: хорошие имена функций делают код самодокументируемым.

**Механика (простой случай)**:
1. Удалите ненужные параметры
2. Измените имя
3. Добавьте нужные параметры
4. Протестируйте

**Механика (миграция — для сложных изменений)**:
1. Если удаляете параметр, убедитесь, что он не используется
2. Создайте новую функцию с нужным объявлением
3. Пусть старая функция вызывает новую
4. Протестируйте
5. Переключите вызывающий код на новую функцию
6. Тестируйте после каждого изменения
7. Удалите старую функцию

**До**:
```javascript
function circum(radius) {
  return 2 * Math.PI * radius;
}
```

**После**:
```javascript
function circumference(radius) {
  return 2 * Math.PI * radius;
}
```

---

### Инкапсуляция переменной (Encapsulate Variable)

**Когда применять**: прямой доступ к данным из нескольких мест

**Мотивация**: дать ясную точку доступа для работы с данными.

**Механика**:
1. Создайте функции чтения и записи (getter и setter)
2. Найдите все обращения
3. Замените чтение вызовом getter
4. Замените запись вызовом setter
5. Тестируйте после каждого изменения
6. Ограничьте видимость переменной

**До**:
```javascript
let defaultOwner = { firstName: "Martin", lastName: "Fowler" };

// Используется во многих местах
spaceship.owner = defaultOwner;
```

**После**:
```javascript
let defaultOwnerData = { firstName: "Martin", lastName: "Fowler" };

function defaultOwner() { return defaultOwnerData; }
function setDefaultOwner(arg) { defaultOwnerData = arg; }

spaceship.owner = defaultOwner();
```

---

### Введение объекта-параметра (Introduce Parameter Object)

**Когда применять**: несколько параметров, которые часто идут вместе

**Мотивация**: сгруппировать данные, которые естественно принадлежат друг другу.

**Механика**:
1. Создайте новый класс или структуру для сгруппированных параметров
2. Протестируйте
3. С помощью изменения объявления функции (Change Function Declaration) добавьте новый объект
4. Протестируйте
5. Для каждого параметра группы удалите его из функции и используйте новый объект
6. Тестируйте после каждого шага

**До**:
```javascript
function amountInvoiced(startDate, endDate) { ... }
function amountReceived(startDate, endDate) { ... }
function amountOverdue(startDate, endDate) { ... }
```

**После**:
```javascript
class DateRange {
  constructor(start, end) {
    this.start = start;
    this.end = end;
  }
}

function amountInvoiced(dateRange) { ... }
function amountReceived(dateRange) { ... }
function amountOverdue(dateRange) { ... }
```

---

### Объединение функций в класс (Combine Functions into Class)

**Когда применять**: несколько функций работают с одними и теми же данными

**Мотивация**: сгруппировать функции с данными, над которыми они работают.

**Механика**:
1. Примените инкапсуляцию записи (Encapsulate Record) к общим данным
2. Переместите каждую функцию в класс
3. Тестируйте после каждого перемещения
4. Замените аргументы-данные обращениями к полям класса

**До**:
```javascript
function base(reading) { ... }
function taxableCharge(reading) { ... }
function calculateBaseCharge(reading) { ... }
```

**После**:
```javascript
class Reading {
  constructor(data) { this._data = data; }

  get base() { ... }
  get taxableCharge() { ... }
  get calculateBaseCharge() { ... }
}
```

---

### Разделение фазы (Split Phase)

**Когда применять**: код занимается двумя разными вещами

**Мотивация**: разделить код на отдельные фазы с ясными границами.

**Механика**:
1. Создайте вторую функцию для второй фазы
2. Протестируйте
3. Введите промежуточную структуру данных между фазами
4. Протестируйте
5. Извлеките первую фазу в собственную функцию
6. Протестируйте

**До**:
```javascript
function priceOrder(product, quantity, shippingMethod) {
  const basePrice = product.basePrice * quantity;
  const discount = Math.max(quantity - product.discountThreshold, 0)
    * product.basePrice * product.discountRate;
  const shippingPerCase = (basePrice > shippingMethod.discountThreshold)
    ? shippingMethod.discountedFee : shippingMethod.feePerCase;
  const shippingCost = quantity * shippingPerCase;
  return basePrice - discount + shippingCost;
}
```

**После**:
```javascript
function priceOrder(product, quantity, shippingMethod) {
  const priceData = calculatePricingData(product, quantity);
  return applyShipping(priceData, shippingMethod);
}

function calculatePricingData(product, quantity) {
  const basePrice = product.basePrice * quantity;
  const discount = Math.max(quantity - product.discountThreshold, 0)
    * product.basePrice * product.discountRate;
  return { basePrice, quantity, discount };
}

function applyShipping(priceData, shippingMethod) {
  const shippingPerCase = (priceData.basePrice > shippingMethod.discountThreshold)
    ? shippingMethod.discountedFee : shippingMethod.feePerCase;
  const shippingCost = priceData.quantity * shippingPerCase;
  return priceData.basePrice - priceData.discount + shippingCost;
}
```

---

## Перемещение функций

### Перемещение метода (Move Method)

**Когда применять**: метод больше использует элементы другого класса, чем своего

**Мотивация**: поместить функции рядом с данными, которые они используют чаще всего.

**Механика**:
1. Изучите все элементы программы, которые метод использует в своём классе
2. Проверьте, полиморфен ли метод
3. Скопируйте метод в целевой класс
4. Подгоните под новый контекст
5. Сделайте так, чтобы исходный метод делегировал целевому
6. Протестируйте
7. Подумайте, не удалить ли исходный метод

---

### Перемещение поля (Move Field)

**Когда применять**: поле чаще использует другой класс

**Мотивация**: держать данные рядом с функциями, которые их используют.

**Механика**:
1. Инкапсулируйте поле, если это ещё не сделано
2. Протестируйте
3. Создайте поле в целевом классе
4. Обновите обращения, чтобы они использовали поле целевого класса
5. Протестируйте
6. Удалите исходное поле

---

### Перемещение операторов в функцию (Move Statements into Function)

**Когда применять**: один и тот же код всегда появляется рядом с вызовом функции

**Мотивация**: убрать дублирование, перенеся повторяющийся код в функцию.

**Механика**:
1. Извлеките повторяющийся код в функцию, если это ещё не сделано
2. Переместите операторы в эту функцию
3. Протестируйте
4. Если вызывающему коду больше не нужны отдельные операторы, удалите их

---

### Перемещение операторов к вызывающим (Move Statements to Callers)

**Когда применять**: общее поведение различается у разных вызывающих

**Мотивация**: когда поведение должно различаться, вынесите его из функции.

**Механика**:
1. Примените извлечение метода (Extract Method) к коду, который нужно перенести
2. Примените встраивание метода (Inline Method) к исходной функции
3. Удалите теперь встроенный вызов
4. Перенесите извлечённый код к каждому вызывающему
5. Протестируйте

---

## Организация данных

### Замена простого значения объектом (Replace Primitive with Object)

**Когда применять**: элементу данных нужно больше поведения, чем у простого значения

**Мотивация**: инкапсулировать данные вместе с их поведением.

**Механика**:
1. Примените инкапсуляцию переменной (Encapsulate Variable)
2. Создайте простой класс значения
3. Измените setter так, чтобы он создавал новый экземпляр
4. Измените getter так, чтобы он возвращал значение
5. Протестируйте
6. Добавьте более богатое поведение в новый класс

**До**:
```javascript
class Order {
  constructor(data) {
    this.priority = data.priority; // строка: "high", "rush" и т. д.
  }
}

// Использование
if (order.priority === "high" || order.priority === "rush") { ... }
```

**После**:
```javascript
class Priority {
  constructor(value) {
    if (!Priority.legalValues().includes(value))
      throw new Error(`Invalid priority: ${value}`);
    this._value = value;
  }

  static legalValues() { return ['low', 'normal', 'high', 'rush']; }
  get value() { return this._value; }

  higherThan(other) {
    return Priority.legalValues().indexOf(this._value) >
           Priority.legalValues().indexOf(other._value);
  }
}

// Использование
if (order.priority.higherThan(new Priority("normal"))) { ... }
```

---

### Замена временной переменной вызовом метода (Replace Temp with Query)

**Когда применять**: временная переменная хранит результат выражения

**Мотивация**: сделать код яснее, извлекая выражение в функцию.

**Механика**:
1. Проверьте, что переменной присваивают значение только один раз
2. Извлеките правую часть присваивания в метод
3. Замените обращения к временной переменной вызовом метода
4. Протестируйте
5. Удалите объявление временной переменной и присваивание

**До**:
```javascript
const basePrice = this._quantity * this._itemPrice;
if (basePrice > 1000) {
  return basePrice * 0.95;
} else {
  return basePrice * 0.98;
}
```

**После**:
```javascript
get basePrice() {
  return this._quantity * this._itemPrice;
}

// В методе
if (this.basePrice > 1000) {
  return this.basePrice * 0.95;
} else {
  return this.basePrice * 0.98;
}
```

---

## Упрощение условной логики

### Декомпозиция условного оператора (Decompose Conditional)

**Когда применять**: сложный условный оператор (if-then-else)

**Мотивация**: сделать намерение ясным, извлекая условия и действия.

**Механика**:
1. Примените извлечение метода (Extract Method) к условию
2. Примените извлечение метода (Extract Method) к ветке then
3. Примените извлечение метода (Extract Method) к ветке else (если она есть)

**До**:
```javascript
if (!aDate.isBefore(plan.summerStart) && !aDate.isAfter(plan.summerEnd)) {
  charge = quantity * plan.summerRate;
} else {
  charge = quantity * plan.regularRate + plan.regularServiceCharge;
}
```

**После**:
```javascript
if (isSummer(aDate, plan)) {
  charge = summerCharge(quantity, plan);
} else {
  charge = regularCharge(quantity, plan);
}

function isSummer(date, plan) {
  return !date.isBefore(plan.summerStart) && !date.isAfter(plan.summerEnd);
}

function summerCharge(quantity, plan) {
  return quantity * plan.summerRate;
}

function regularCharge(quantity, plan) {
  return quantity * plan.regularRate + plan.regularServiceCharge;
}
```

---

### Консолидация условного выражения (Consolidate Conditional Expression)

**Когда применять**: несколько условий с одним и тем же результатом

**Мотивация**: сделать явным, что условия — это одна проверка.

**Механика**:
1. Убедитесь, что в условиях нет побочных эффектов
2. Объедините условия с помощью `and` или `or`
3. Подумайте об извлечении метода (Extract Method) для объединённого условия

**До**:
```javascript
if (employee.seniority < 2) return 0;
if (employee.monthsDisabled > 12) return 0;
if (employee.isPartTime) return 0;
```

**После**:
```javascript
if (isNotEligibleForDisability(employee)) return 0;

function isNotEligibleForDisability(employee) {
  return employee.seniority < 2 ||
         employee.monthsDisabled > 12 ||
         employee.isPartTime;
}
```

---

### Замена вложенного условного оператора граничными (Replace Nested Conditional with Guard Clauses)

**Когда применять**: глубоко вложенные условия, из-за которых поток трудно проследить

**Мотивация**: используйте граничные операторы для особых случаев, сохраняя обычный поток ясным.

**Механика**:
1. Найдите условия особых случаев
2. Замените их граничными операторами с ранним возвратом
3. Тестируйте после каждого изменения

**До**:
```javascript
function payAmount(employee) {
  let result;
  if (employee.isSeparated) {
    result = { amount: 0, reasonCode: "SEP" };
  } else {
    if (employee.isRetired) {
      result = { amount: 0, reasonCode: "RET" };
    } else {
      result = calculateNormalPay(employee);
    }
  }
  return result;
}
```

**После**:
```javascript
function payAmount(employee) {
  if (employee.isSeparated) return { amount: 0, reasonCode: "SEP" };
  if (employee.isRetired) return { amount: 0, reasonCode: "RET" };
  return calculateNormalPay(employee);
}
```

---

### Замена условного оператора полиморфизмом (Replace Conditional with Polymorphism)

**Когда применять**: switch/case по типу, условная логика, которая меняется в зависимости от типа

**Мотивация**: пусть объекты сами обрабатывают своё поведение.

**Механика**:
1. Создайте иерархию классов (если её ещё нет)
2. Используйте фабричную функцию (Factory Function) для создания объектов
3. Перенесите условную логику в метод суперкласса
4. Создайте метод подкласса для каждой ветки
5. Удалите исходное условие

**До**:
```javascript
function plumages(birds) {
  return birds.map(b => plumage(b));
}

function plumage(bird) {
  switch (bird.type) {
    case 'EuropeanSwallow':
      return "average";
    case 'AfricanSwallow':
      return (bird.numberOfCoconuts > 2) ? "tired" : "average";
    case 'NorwegianBlueParrot':
      return (bird.voltage > 100) ? "scorched" : "beautiful";
    default:
      return "unknown";
  }
}
```

**После**:
```javascript
class Bird {
  get plumage() { return "unknown"; }
}

class EuropeanSwallow extends Bird {
  get plumage() { return "average"; }
}

class AfricanSwallow extends Bird {
  get plumage() {
    return (this.numberOfCoconuts > 2) ? "tired" : "average";
  }
}

class NorwegianBlueParrot extends Bird {
  get plumage() {
    return (this.voltage > 100) ? "scorched" : "beautiful";
  }
}

function createBird(data) {
  switch (data.type) {
    case 'EuropeanSwallow': return new EuropeanSwallow(data);
    case 'AfricanSwallow': return new AfricanSwallow(data);
    case 'NorwegianBlueParrot': return new NorwegianBlueParrot(data);
    default: return new Bird(data);
  }
}
```

---

### Введение особого случая (Introduce Special Case, Null Object)

**Когда применять**: повторяющиеся проверки на null для особых случаев

**Мотивация**: возвращать особый объект, который обрабатывает особый случай.

**Механика**:
1. Создайте класс особого случая с ожидаемым интерфейсом
2. Добавьте проверку isSpecialCase
3. Введите фабричный метод
4. Замените проверки на null использованием объекта особого случая
5. Протестируйте

**До**:
```javascript
const customer = site.customer;
// ... проверки во многих местах
if (customer === "unknown") {
  customerName = "occupant";
} else {
  customerName = customer.name;
}
```

**После**:
```javascript
class UnknownCustomer {
  get name() { return "occupant"; }
  get billingPlan() { return registry.defaultPlan; }
}

// Фабричный метод
function customer(site) {
  return site.customer === "unknown"
    ? new UnknownCustomer()
    : site.customer;
}

// Использование — проверки на null не нужны
const customerName = customer.name;
```

---

## Рефакторинг API

### Отделение запроса от модификатора (Separate Query from Modifier)

**Когда применять**: функция и возвращает значение, и имеет побочные эффекты

**Мотивация**: сделать ясным, какие операции имеют побочные эффекты.

**Механика**:
1. Создайте новую функцию-запрос
2. Скопируйте логику возврата исходной функции
3. Измените исходную так, чтобы она возвращала void
4. Замените вызовы, которые используют возвращаемое значение
5. Протестируйте

**До**:
```javascript
function alertForMiscreant(people) {
  for (const p of people) {
    if (p === "Don") {
      setOffAlarms();
      return "Don";
    }
    if (p === "John") {
      setOffAlarms();
      return "John";
    }
  }
  return "";
}
```

**После**:
```javascript
function findMiscreant(people) {
  for (const p of people) {
    if (p === "Don") return "Don";
    if (p === "John") return "John";
  }
  return "";
}

function alertForMiscreant(people) {
  if (findMiscreant(people) !== "") setOffAlarms();
}
```

---

### Параметризация функции (Parameterize Function)

**Когда применять**: несколько функций делают похожее с разными значениями

**Мотивация**: убрать дублирование, добавив параметр.

**Механика**:
1. Выберите одну функцию
2. Добавьте параметр для изменяющегося литерала
3. Измените тело так, чтобы оно использовало параметр
4. Протестируйте
5. Переключите вызывающий код на параметризованную версию
6. Удалите теперь неиспользуемые функции

**До**:
```javascript
function tenPercentRaise(person) {
  person.salary = person.salary * 1.10;
}

function fivePercentRaise(person) {
  person.salary = person.salary * 1.05;
}
```

**После**:
```javascript
function raise(person, factor) {
  person.salary = person.salary * (1 + factor);
}

// Использование
raise(person, 0.10);
raise(person, 0.05);
```

---

### Удаление аргумента-флага (Remove Flag Argument)

**Когда применять**: логический параметр, который меняет поведение функции

**Мотивация**: сделать поведение явным через отдельные функции.

**Механика**:
1. Создайте явную функцию для каждого значения флага
2. Замените каждый вызов подходящей новой функцией
3. Тестируйте после каждого изменения
4. Удалите исходную функцию

**До**:
```javascript
function bookConcert(customer, isPremium) {
  if (isPremium) {
    // логика премиум-бронирования
  } else {
    // логика обычного бронирования
  }
}

bookConcert(customer, true);
bookConcert(customer, false);
```

**После**:
```javascript
function bookPremiumConcert(customer) {
  // логика премиум-бронирования
}

function bookRegularConcert(customer) {
  // логика обычного бронирования
}

bookPremiumConcert(customer);
bookRegularConcert(customer);
```

---

## Работа с наследованием

### Подъём метода (Pull Up Method)

**Когда применять**: один и тот же метод в нескольких подклассах

**Мотивация**: убрать дублирование в иерархии классов.

**Механика**:
1. Просмотрите методы и убедитесь, что они одинаковы
2. Проверьте, что сигнатуры совпадают
3. Создайте новый метод в суперклассе
4. Скопируйте тело из одного подкласса
5. Удалите метод одного подкласса, протестируйте
6. Удалите методы остальных подклассов, тестируя каждый

---

### Спуск метода (Push Down Method)

**Когда применять**: поведение нужно лишь подмножеству подклассов

**Мотивация**: поместить метод туда, где он используется.

**Механика**:
1. Скопируйте метод в каждый подкласс, которому он нужен
2. Удалите метод из суперкласса
3. Протестируйте
4. Удалите его из подклассов, которым он не нужен
5. Протестируйте

---

### Замена подкласса делегатом (Replace Subclass with Delegate)

**Когда применять**: наследование используется неверно, нужна большая гибкость

**Мотивация**: предпочитайте композицию наследованию, когда это уместно.

**Механика**:
1. Создайте пустой класс для делегата
2. Добавьте классу-владельцу поле, хранящее делегат
3. Создайте конструктор делегата, который вызывается из класса-владельца
4. Перенесите элементы в делегат
5. Тестируйте после каждого переноса
6. Замените наследование делегированием

---

## Извлечение класса (Extract Class)

**Когда применять**: большой класс с несколькими ответственностями

**Мотивация**: разделить класс, чтобы сохранить единственную ответственность.

**Механика**:
1. Решите, как разделить ответственности
2. Создайте новый класс
3. Перенесите поле из исходного класса в новый
4. Протестируйте
5. Перенесите методы из исходного класса в новый
6. Тестируйте после каждого переноса
7. Просмотрите и переименуйте оба класса
8. Решите, как открыть доступ к новому классу

**До**:
```javascript
class Person {
  get name() { return this._name; }
  set name(arg) { this._name = arg; }
  get officeAreaCode() { return this._officeAreaCode; }
  set officeAreaCode(arg) { this._officeAreaCode = arg; }
  get officeNumber() { return this._officeNumber; }
  set officeNumber(arg) { this._officeNumber = arg; }

  get telephoneNumber() {
    return `(${this._officeAreaCode}) ${this._officeNumber}`;
  }
}
```

**После**:
```javascript
class Person {
  constructor() {
    this._telephoneNumber = new TelephoneNumber();
  }
  get name() { return this._name; }
  set name(arg) { this._name = arg; }
  get telephoneNumber() { return this._telephoneNumber.toString(); }
  get officeAreaCode() { return this._telephoneNumber.areaCode; }
  set officeAreaCode(arg) { this._telephoneNumber.areaCode = arg; }
}

class TelephoneNumber {
  get areaCode() { return this._areaCode; }
  set areaCode(arg) { this._areaCode = arg; }
  get number() { return this._number; }
  set number(arg) { this._number = arg; }
  toString() { return `(${this._areaCode}) ${this._number}`; }
}
```

---

## Краткий справочник: от запаха к рефакторингу

| Запах кода | Основной рефакторинг | Альтернатива |
|------------|----------------------|--------------|
| Длинный метод | Извлечение метода (Extract Method) | Замена временной переменной вызовом метода (Replace Temp with Query) |
| Дублирование кода | Извлечение метода (Extract Method) | Подъём метода (Pull Up Method) |
| Большой класс | Извлечение класса (Extract Class) | Извлечение подкласса (Extract Subclass) |
| Длинный список параметров | Введение объекта-параметра (Introduce Parameter Object) | Сохранение всего объекта (Preserve Whole Object) |
| Зависть к функциям | Перемещение метода (Move Method) | Извлечение метода (Extract Method) + перемещение |
| Группы данных | Извлечение класса (Extract Class) | Введение объекта-параметра (Introduce Parameter Object) |
| Одержимость элементарными типами | Замена простого значения объектом (Replace Primitive with Object) | Замена кода типа (Replace Type Code) |
| Операторы switch | Замена условного оператора полиморфизмом (Replace Conditional with Polymorphism) | Замена кода типа (Replace Type Code) |
| Временное поле | Извлечение класса (Extract Class) | Введение объекта Null (Introduce Null Object) |
| Цепочки сообщений | Сокрытие делегата (Hide Delegate) | Извлечение метода (Extract Method) |
| Посредник | Удаление посредника (Remove Middle Man) | Встраивание метода (Inline Method) |
| Расходящиеся модификации | Извлечение класса (Extract Class) | Разделение фазы (Split Phase) |
| Стрельба дробью | Перемещение метода (Move Method) | Встраивание класса (Inline Class) |
| Мёртвый код | Удаление мёртвого кода (Remove Dead Code) | — |
| Теоретическая общность | Свёртывание иерархии (Collapse Hierarchy) | Встраивание класса (Inline Class) |

---

## Дополнительное чтение

- Fowler, M. (2018). *Refactoring: Improving the Design of Existing Code* (2nd ed.) — «Рефакторинг. Улучшение проекта существующего кода»
- Онлайн-каталог: https://refactoring.com/catalog/

---

**Последнее обновление**: 4 августа 2026
**Версия Claude Code**: 2.1.220
**Источники**:
- https://code.claude.com/docs/en/skills
**Совместимые модели**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
