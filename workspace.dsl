workspace {
    name "File Storage System"
    !identifiers hierarchical

    model {
        user = person "Пользователь" {
            description "Пользователь системы хранения файлов"
        }

        fileStorageSystem = softwareSystem "Система хранения файлов" {
            description "Облачное хранилище для управления файлами и папками"

            authService = container "Auth Service" {
                technology "Python / FastAPI"
                description "Сервис аутентификации и управления пользователями"
            }

            fileService = container "File Service" {
                technology "Python / FastAPI"
                description "Сервис управления файлами"
            }

            folderService = container "Folder Service" {
                technology "Python / FastAPI"
                description "Сервис управления папками"
            }

            userDatabase = container "User Database" {
                technology "PostgreSQL"
                description "База данных пользователей"
            }

            fileDatabase = container "File Database" {
                technology "MongoDB"
                description "База данных файлов"
            }

            folderDatabase = container "Folder Database" {
                technology "MongoDB"
                description "База данных папок"
            }

            // Взаимодействие
            user -> authService "Регистрация и аутентификация" "REST"
            authService -> userDatabase "Сохраняет и получает данные о пользователях" "JDBC"
            user -> authService "Поиск пользователя по логину" "REST"
            authService -> userDatabase "Находит пользователя по логину" "JDBC"
            user -> authService "Поиск пользователя по имени и фамилии" "REST"
            authService -> userDatabase "Находит пользователя по имени и фамилии" "JDBC"

            user -> folderService "Создает папки" "REST"
            folderService -> folderDatabase "Сохраняет информацию о папках" "MongoDB"
            user -> folderService "Получает список папок" "REST"
            folderService -> folderDatabase "Читает список папок" "MongoDB"

            user -> fileService "Загружает файл" "REST"
            fileService -> fileDatabase "Сохраняет информацию о файлах" "MongoDB"
            user -> fileService "Получает файл по имени" "REST"
            fileService -> fileDatabase "Читает файл по имени" "MongoDB"

            user -> fileService "Удаляет файл" "REST"
            fileService -> fileDatabase "Удаляет информацию о файле" "MongoDB"
            user -> folderService "Удаляет папку" "REST"
            folderService -> folderDatabase "Удаляет информацию о папке" "MongoDB"
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
            user -> fileStorageSystem.authService "Отправляет запрос на создание пользователя"
            fileStorageSystem.authService -> fileStorageSystem.userDatabase "Сохраняет данные"
            fileStorageSystem.authService -> user "Подтверждает регистрацию"
        }

        dynamic fileStorageSystem "search_user_by_login" "Поиск пользователя по логину" {
            autoLayout lr
            user -> fileStorageSystem.authService "Запрашивает поиск по логину"
            fileStorageSystem.authService -> fileStorageSystem.userDatabase "Получает данные пользователя"
            fileStorageSystem.authService -> user "Отправляет данные"
        }

        dynamic fileStorageSystem "search_user_by_name" "Поиск пользователя по имени и фамилии" {
            autoLayout lr
            user -> fileStorageSystem.authService "Запрашивает поиск по имени и фамилии"
            fileStorageSystem.authService -> fileStorageSystem.userDatabase "Получает данные пользователя"
            fileStorageSystem.authService -> user "Отправляет данные"
        }

        dynamic fileStorageSystem "create_folder" "Создание новой папки" {
            autoLayout lr
            user -> fileStorageSystem.folderService "Запрашивает создание папки"
            fileStorageSystem.folderService -> fileStorageSystem.folderDatabase "Сохраняет данные о папке"
            fileStorageSystem.folderService -> user "Подтверждает создание папки"
        }

        dynamic fileStorageSystem "get_folders" "Получение списка папок" {
            autoLayout lr
            user -> fileStorageSystem.folderService "Запрашивает список папок"
            fileStorageSystem.folderService -> fileStorageSystem.folderDatabase "Получает список папок"
            fileStorageSystem.folderService -> user "Возвращает список папок"
        }

        dynamic fileStorageSystem "upload_file" "Загрузка файла" {
            autoLayout lr
            user -> fileStorageSystem.fileService "Отправляет файл на сервер"
            fileStorageSystem.fileService -> fileStorageSystem.fileDatabase "Сохраняет метаданные файла"
            fileStorageSystem.fileService -> user "Подтверждает загрузку файла"
        }
    }
}
