import React from 'react';

const About: React.FC = () => {
  return (
    <main className="flex-1 flex flex-col items-center bg-gray-100 overflow-auto">
      <div className="w-full max-w-2xl bg-white rounded-lg shadow-md p-8 my-8">
        <h1 className="text-3xl font-bold mb-4 text-center text-gray-700">Gerber to PNG Converter</h1>
        <div className="text-left text-gray-1000">
          <p className="mb-4">
            Веб-сервис для конвертации Gerber и Drill файлов экспортированных из KiCad в PNG изображение.
            Для последующей засветки платы на фотополимерном принтере.
          </p>
          <p className="text-sm">
            Я увлекаюсь электроникой и часто делаю печатные платы в домашних условиях.<br />
            Для этого я использую фотополимерный принтер для переноса разводки печатной платы на стеклотекстолит, который предварительно покрыт фоторезистом.<br />
            Я экспортирую разводку из KiCad в Gerber и Drill форматы, затем конвертирую их в PNG изображение с помощью этого сервиса.<br />
            Полученное изображение загружаю в приложения UVTools и преобразую в файл подходящий для моего принтера.<br />
          </p>
          <div className="mt-8"></div>
          <h2 className="text-2xl font-bold mb-4 text-left text-gray-1000">Краткая инструкция по использованию</h2>
          <h3 className="text-xl font-bold mb-4 text-left text-gray-1000">1. Экспорт разводки из KiCad</h3>
          <p className="mb-4">
            
            <img src="/images/kicad01.png" alt="KiCad export" className="w-full h-auto" />
            <ol>
                <li>1. Устанавливаем Origin point на нижний левый угол.</li>
                <li>2. Жмем на кнопку "Plot".</li>
            </ol>
            
            <img src="/images/kicad02.png" alt="KiCad export" className="w-full h-auto" />
            <ol>
                <li>3. Выбираем формат Gerber в разделе "Plot format".</li>
                <li>4. Выбираем нужные нам слои, например "F.Cu".</li>
                <li>5. Ставим галочку на "Use drill/place file origin".</li>
                <li>6. Жмем на кнопку "Plot" - так мы получим файл с разводкой и расширением .gbr</li>
                <li>7. Жмем на кнопку "Generate Drill Files..." - откроется окно с настройками для экспорта файла с отверстиями</li>
            </ol>
            
            <img src="/images/kicad03.png" alt="KiCad export" className="w-full h-auto" />
            <ol>
                <li>8. Снимаем галку "Mirror Y axis".</li>
                <li>9. В разделе "Gerber Drill File" - так мы получим файл с разводкой и расширением .gbr</li>
            </ol>
            Можно переходить к следующему шагу.

            <div className="mt-8"></div>
            <h3 className="text-xl font-bold mb-4 text-left text-gray-1000">2. Загрузка файлов в сервис</h3>
            <p className="mb-4">
                <ol>
                <li>1. Выбираем свой принтер из выпадающего списка. Например, Anycubic Photon M3.</li>
                <li>2. Ставим галки для отражения по вертикали/горизонтали, если это необходимо.</li>
                <li>3. Загружаем полученные файлы в сервис.</li>
                <li>4. Жмем на кнопку "Send".</li>
                <li>5. Ждем пока сервис сконвертирует файлы и скачаем результат в формате .png.</li>
                </ol>
            </p>

            <div className="mt-8"></div>
            <h3 className="text-xl font-bold mb-4 text-left text-gray-1000">3. Обработка файла в приложения <a href="https://github.com/sn4k3/UVtools" target="_blank" rel="noopener noreferrer" className="underline">UVTools</a></h3>
            <p className="mb-4">
                
                <ul>
                    <li>1. открываем <a href="https://github.com/sn4k3/UVtools" target="_blank" rel="noopener noreferrer" className="underline">UVTools</a></li>
                    <li>2. Меняем размер дефолтного изображения до 30%, иначе вылетает ошибка: <b>Tools -{'>'} Resize -{'>'} 30%</b></li>
                    <li>3. Отключаем вращение: <b>Disable Rotation</b></li>
                    <li>4. Выбираем принтер: <b>Tools -{'>'} Change print resolution -{'>'} Select printer (мой Anycubic Photon M3)</b></li>
                    <li>5. Импортируем слои: <b>Actions -{'>'} Import layers</b></li>
                    <li>5.1 Выбираем тип импорта: <b>Import type -{'>'} Insert</b></li>
                    <li>5.2 Добавляем файл наш PNG файл: <b>Add -{'>'} Select PNG -{'>'} Import</b></li>
                    <li>6. Удаляем слои 1-10: <b>Actions -{'>'} Remove layers -{'>'} 1 - 10</b></li>
                    <li>7. Перемещаем изображение: <b>Tools -{'>'} Move -{'>'} select top/left corner</b></li>
                    <li>7.1 Выставляем координаты: <b>Top 250 (для моего принтера = 10mm)</b></li>
                    <li>7.2 Выставляем координаты: <b>Left 250 (для моего принтера = 10mm)</b></li>
                    <li>8. Устанавливаем время засветки: <b>Left Menu -{'>'} Exposure Time = 30s</b></li>
                    <li>9. Заменяем изображение preview (не обязательно): <b>Replace preview images</b></li>
                    <li>10. Конвертируем в файл для принтера: <b>File -{'>'} Convert to -{'>'} Anycubic -{'>'} Photon M3 (Add extension: .pm3)</b></li>
                </ul>
            </p>
          </p>
        </div>
      </div>
    </main>
  );
};

export default About;
