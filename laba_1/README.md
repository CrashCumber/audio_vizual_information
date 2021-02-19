# Лабораторная работа 1. Передискретизация, обесцвечивание и бинаризация растровых изображений

## 1. Передискретизация
1) Исходное изображение
   
![Исходное изображение](images/eye.jpg)
   
2) Растяжение (интерполяция) изображения в M = 4 раз.

![Получившееся изображение](result_images/sampling/img_up.png)
   
3) Сжатие (децимация) изображения в N = 3 раз.   
   
![Получившееся изображение](result_images/sampling/img_down.png)
   
4) Передискретизация изображения в K = 4/3 раз путём растяжения и
последующего сжатия (в два прохода).
   
![Получившееся изображение](result_images/sampling/img_samp_two.png)
   
5) Передискретизация изображения в K раз за один проход.  
   
![Получившееся изображение](result_images/sampling/img_samp_one.png)
   
## 2. Приведение полноцветного изображения к полутоновому.
1) Исходное изображение
   
![Исходное изображение](images/cat.jpg)
   
2) Создание нового изображения в режиме полутона (1 яркостный канал).
   
3) Попиксельный расчёт яркости нового изображения на основе полноцветного
путём усреднения по каналам.
   
4) Получившееся изображение.
   
![Получившееся изображение](result_images/img_s.png)

## 3. Приведение полутонового изображения к монохромному методом пороговой обработки. Один алгоритм на выбор:

### Улучшенный алгоритм адаптивной бинаризации Бернсена.

В зависимости от рода изображения задается разный коэффициент INDENT.  
INDENT - отступ от рассчитываемого пикселя. На его основе рассчитывается площадь и средняя яркость зоны вокруг пикселя.    

**Темно-зеленым цветом обозначается рассчитываемый пиксель.
Коралловым - отступы(INDENT)**   

**INDENT = 3**

![](images/exm_indent.png)

**INDENT = 2**  

![](images/exm_indent_2.png)

Было замечено, что для бинаризации мелкими деталями(текст) наиболее подходит небольшое значение данного коэффициента (< 10).При задание большего значения
появляются шумы и пропадает четкость.
  
Для изображений с выраженными деталями(человек, предметы, композиция) удобно использовать коэффициента > 20. При задании меньшего коэффициента
детали становятся неярко выражены.

### Пример:
1) INDENT = 3 

Обработка текста: 
   
   ![текст](result_images/binary_images/text_indent_3.png)


Обработка картинки:

   ![глаз](result_images/binary_images/eye_indent_3.png)

2) INDENT = 20 


Обработка текста: 

   ![текст](result_images/binary_images/text_indent_20.png)


Обработка картинки:

   ![глаз](result_images/binary_images/eye_indent_20.png)

## Где использовать бинаризацию
Бинаризация плохо подходит для обработки изображений-фото, где преобладают либо светлые, либо темные оттенки. Картинка 
в результате получается трудно разборчивая, элементы плохо различаются.

Для текстов или элементов с явно выраженными различиями в цветах, картинок с высокой контрастностью бинаризация дает понятный и различимый результат.

### Пример 
 - Исходное изображение

![dogs](images/dogs.jpg)

- INDENT = 20

![dogs](result_images/binary_images/dogs_indent_20.png)

- INDENT = 10

![dogs](result_images/binary_images/dogs_indent_10.png)

- INDENT = 5

![dogs](result_images/binary_images/dogs_indent_5.png)