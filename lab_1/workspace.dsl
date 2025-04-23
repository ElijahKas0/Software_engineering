workspace { 
    name "File Storage System"
    !identifiers hierarchical

    model {
        user = person "Пользователь" {
            description "Пользователь системы хранения файлов"
        }

        fileStorageSystem = softwareSystem "Система хранения файлов" {
            description "Облачное хранилище для управления файлами и папками"

            userApiService = container "User API Service" {
                technology "Python / FastAPI"
                description "Сервис аутентификации и управления пользователями"
            }

            fileStorageService = container "File Storage Service" {
                technology "Python / FastAPI"
                description "Сервис управления файлами, валидации прав и обработки загрузок"
            }

            folderService = container "Folder Service" {
                technology "Python / FastAPI"
                description "Сервис управления папками"
            }

            userDatabase = container "User Database" {
                technology "PostgreSQL"
                description "База данных пользователей (PostgreSQL)"
            }

            fileDatabase = container "File Database" {
                technology "MongoDB"
                description "База данных файлов (MongoDB)"
            }

            folderDatabase = container "Folder Database" {
                technology "MongoDB"
                description "База данных папок (MongoDB)"
            }

            // Взаимодействие
            user -> userApiService "Регистрация и аутентификация" "REST"
            user -> userApiService "Поиск пользователя по логину/имени" "REST"
            userApiService -> userDatabase "Чтение и запись данных" "JDBC"

            user -> folderService "Создает/удаляет папки" "REST"
            folderService -> folderDatabase "Работает с информацией о папках" "MongoDB"

            user -> fileStorageService "Загружает/удаляет файлы" "REST"
            fileStorageService -> fileDatabase "Хранит метаданные файлов" "MongoDB"

            fileStorageService -> fileDatabase "Проверяет права и владельца" "MongoDB"
        }
    }

    views {
        themes default

        systemContext fileStorageSystem {
            include *
            autolayout lr
        }

        container fileStorageSystem {
            include *
            autolayout lr
        }

        dynamic fileStorageSystem "create_user" "Создание нового пользователя" {
            autoLayout lr
            user -> fileStorageSystem.userApiService "Отправляет запрос на создание пользователя"
            fileStorageSystem.userApiService -> fileStorageSystem.userDatabase "Сохраняет данные"
            fileStorageSystem.userApiService -> user "Подтверждает регистрацию"
        }

        dynamic fileStorageSystem "search_user" "Поиск пользователя" {
            autoLayout lr
            user -> fileStorageSystem.userApiService "Отправляет запрос на поиск"
            fileStorageSystem.userApiService -> fileStorageSystem.userDatabase "Читает данные"
            fileStorageSystem.userApiService -> user "Отправляет результат"
        }

        dynamic fileStorageSystem "upload_file" "Загрузка файла пользователем" {
            autoLayout lr
            user -> fileStorageSystem.fileStorageService "Отправляет файл"
            fileStorageSystem.fileStorageService -> fileStorageSystem.fileDatabase "Сохраняет метаданные"
            fileStorageSystem.fileStorageService -> user "Подтверждает загрузку"
        }

        dynamic fileStorageSystem "delete_own_file" "Удаление собственного файла" {
            autoLayout lr
            user -> fileStorageSystem.fileStorageService "Запрашивает удаление"
            fileStorageSystem.fileStorageService -> fileStorageSystem.fileDatabase "Проверяет владельца"
            fileStorageSystem.fileStorageService -> fileStorageSystem.fileDatabase "Удаляет файл"
            fileStorageSystem.fileStorageService -> user "Подтверждает удаление"
        }

        dynamic fileStorageSystem "admin_delete_other_file" "Удаление чужого файла админом" {
            autoLayout lr
            user -> fileStorageSystem.fileStorageService "Админ отправляет запрос"
            fileStorageSystem.fileStorageService -> fileStorageSystem.fileDatabase "Находит файл"
            fileStorageSystem.fileStorageService -> fileStorageSystem.fileDatabase "Удаляет файл"
            fileStorageSystem.fileStorageService -> user "Подтверждает удаление"
        }

        dynamic fileStorageSystem "create_folder" "Создание новой папки" {
            autoLayout lr
            user -> fileStorageSystem.folderService "Запрашивает создание"
            fileStorageSystem.folderService -> fileStorageSystem.folderDatabase "Сохраняет информацию"
            fileStorageSystem.folderService -> user "Подтверждает создание"
        }

        dynamic fileStorageSystem "get_folders" "Получение списка папок" {
            autoLayout lr
            user -> fileStorageSystem.folderService "Запрашивает список"
            fileStorageSystem.folderService -> fileStorageSystem.folderDatabase "Читает из БД"
            fileStorageSystem.folderService -> user "Возвращает список"
        }
    }
}
