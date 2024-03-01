CREATE TABLE Mariners (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstName VARCHAR(255) NOT NULL,
    lastName VARCHAR(255) NOT NULL,
    marinersIdNumber VARCHAR(255) NOT NULL UNIQUE,
    address TEXT,
    email VARCHAR(255) NOT NULL UNIQUE,
    phoneNumber VARCHAR(20),
    dateJoined DATE,
    status ENUM('active', 'inactive') NOT NULL
);

CREATE TABLE StaffAdmin (
    staffNumber INT AUTO_INCREMENT PRIMARY KEY,
    firstName VARCHAR(255) NOT NULL,
    lastName VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    workPhoneNumber VARCHAR(20),
    hireDate DATE,
    position VARCHAR(255),
    department VARCHAR(255),
    status ENUM('active', 'inactive') NOT NULL
);
CREATE TABLE OceanPestDiseaseGuide (
    OceanID INT AUTO_INCREMENT PRIMARY KEY,
    ItemType ENUM('pest', 'disease') NOT NULL,
    PresentInNZ BOOLEAN NOT NULL,
    CommonName VARCHAR(255) NOT NULL,
    ScientificName VARCHAR(255),
    KeyCharacteristics TEXT,
    BiologyDescription TEXT,
    Threats TEXT,
    Location TEXT,
    ImageURLs TEXT,
    PrimaryImageURL VARCHAR(255)
);
