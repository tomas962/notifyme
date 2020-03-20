-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Mar 20, 2020 at 10:19 PM
-- Server version: 5.7.29-0ubuntu0.18.04.1
-- PHP Version: 7.2.24-0ubuntu0.18.04.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `notify`
--

-- --------------------------------------------------------

--
-- Table structure for table `car_make`
--

CREATE TABLE `car_make` (
  `car_id` int(11) NOT NULL,
  `make_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `car_make`
--

INSERT INTO `car_make` (`car_id`, `make_id`) VALUES
(3, 175);

-- --------------------------------------------------------

--
-- Table structure for table `car_queries`
--

CREATE TABLE `car_queries` (
  `id` int(11) NOT NULL,
  `price_from` int(11) DEFAULT NULL,
  `price_to` int(11) DEFAULT NULL,
  `year_from` int(11) DEFAULT NULL,
  `search_term` text,
  `year_to` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `car_queries`
--

INSERT INTO `car_queries` (`id`, `price_from`, `price_to`, `year_from`, `search_term`, `year_to`) VALUES
(1, 1000, 2000, 2000, 'audi', 2010),
(3, 1222, 1333, 2000, 'kfgukj', 2005),
(6, NULL, NULL, NULL, NULL, NULL),
(7, NULL, NULL, NULL, NULL, NULL),
(8, NULL, NULL, NULL, NULL, NULL),
(9, NULL, NULL, NULL, 'test', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `makes`
--

CREATE TABLE `makes` (
  `make` varchar(100) DEFAULT NULL,
  `id` int(11) NOT NULL,
  `autoplius_make_id` int(11) DEFAULT NULL,
  `autobilis_make_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `makes`
--

INSERT INTO `makes` (`make`, `id`, `autoplius_make_id`, `autobilis_make_id`) VALUES
('All', 1, NULL, NULL),
('AC', 2, 105, 136),
('Acura', 3, 104, 9002),
('Aixam', 4, 108, 137),
('Alfa-Romeo', 5, 103, 138),
('Alpina', 6, 112, 139),
('Aro', 7, 102, NULL),
('Asia', 8, 101, NULL),
('Audi', 10, 99, 143),
('Austin', 11, NULL, 144),
('Autobianchi', 12, NULL, NULL),
('Baic', 13, NULL, NULL),
('Bellier', 14, 28319, NULL),
('Bentley', 15, 98, 145),
('BMW', 16, 97, 146),
('Brilliance', 17, 19319, NULL),
('Bugatti', 18, 19781, 148),
('Buick', 19, 96, 149),
('Cadillac', 20, 95, 150),
('Casalini', 21, NULL, NULL),
('Caterham', 22, NULL, 151),
('Chatenet', 23, NULL, NULL),
('Chevrolet', 24, 94, 153),
('Chrysler', 25, 93, 154),
('Citroen', 26, 92, 155),
('CityEL', 27, NULL, NULL),
('Comarth', 28, NULL, NULL),
('Dacia', 29, 110, 157),
('Daewoo', 30, 91, 158),
('DAF', 31, 25072, NULL),
('Daihatsu', 32, 90, 159),
('DFSK', 34, NULL, NULL),
('DKW', 35, NULL, NULL),
('Dodge', 36, 89, 162),
('Eagle', 37, 88, NULL),
('FAW', 38, NULL, NULL),
('Ferrari', 39, 87, 163),
('Fiat', 40, 86, 164),
('Fisker', 41, 18542, 8965),
('Ford', 42, 85, 165),
('Galloper', 43, NULL, NULL),
('GAZ', 44, 109, 10028),
('Geely', 45, NULL, NULL),
('Genesis', 46, NULL, NULL),
('GMC', 47, 41, 166),
('Gonow', 48, 19091, NULL),
('Goupil', 49, NULL, NULL),
('Grecav', 50, NULL, NULL),
('GWM', 51, NULL, NULL),
('Holden', 52, NULL, NULL),
('Honda', 53, 84, 169),
('Hummer', 54, 83, 171),
('Hyundai', 55, 82, 172),
('Infiniti', 56, 81, 173),
('Isuzu', 57, 80, 174),
('Iveco', 58, 125, 8690),
('Jaguar', 59, 79, 175),
('Jeep', 60, 78, 176),
('Kaipan', 61, NULL, NULL),
('Kia', 62, 77, 178),
('Koenigsegg', 63, 18799, 179),
('Lada', 64, 76, 180),
('Lamborghini', 65, 75, 181),
('Lancia', 66, 74, 182),
('Land-Rover', 67, NULL, 183),
('Landwind', 68, 123, NULL),
('LDV', 69, 28061, 9976),
('Lexus', 70, 72, 184),
('Ligier', 71, 18723, 10023),
('Lincoln', 72, 71, 185),
('Lotus', 73, 70, 187),
('LTI', 74, NULL, 188),
('LuAZ', 75, 119, NULL),
('Mahindra', 76, 16535, NULL),
('Man', 77, NULL, NULL),
('Maruti', 78, NULL, NULL),
('Maserati', 79, 69, 189),
('Maybach', 80, 111, 190),
('Mazda', 81, 68, 191),
('McLaren', 82, 24629, NULL),
('Mercedes-Benz', 83, 67, 192),
('Mercury', 84, 66, 193),
('MG', 85, 65, 194),
('Microcar', 86, 16127, 196),
('MINI', 87, 64, 197),
('Mitsubishi', 88, 63, 198),
('Morgan', 89, 17392, 200),
('Moskvich', 90, 116, 9018),
('Nissan', 91, 62, 202),
('NSU', 92, NULL, NULL),
('Nysa', 93, 24732, NULL),
('Oldsmobile', 94, 61, 204),
('Oltcit', 95, NULL, NULL),
('Opel', 96, 60, 205),
('Peugeot', 97, 59, 209),
('Piaggio', 98, NULL, NULL),
('Pinzgauer', 99, NULL, NULL),
('Plymouth', 100, 58, 211),
('Polonez', 101, NULL, NULL),
('Pontiac', 102, 57, 212),
('Porsche', 103, 56, 213),
('Proton', 104, 55, 214),
('Renault', 105, 54, 218),
('Rolls-Royce', 106, 53, 223),
('Rover', 107, 52, 224),
('Saab', 108, 51, 225),
('Samsung', 109, NULL, NULL),
('Santana', 110, 107, 226),
('Saturn', 111, 50, 227),
('Scion', 112, 114, 10043),
('Seat', 113, 49, 228),
('Shuanghuan', 114, 10861, NULL),
('Skoda', 115, 48, 229),
('Smart', 116, 47, 230),
('Ssangyong', 117, 40, 232),
('Subaru', 118, 46, 234),
('Suzuki', 119, 45, 235),
('Syrena', 120, NULL, NULL),
('Talbot', 121, 21501, 236),
('Tarpan', 122, NULL, NULL),
('Tata', 123, 10863, 237),
('Tatra', 124, 120, NULL),
('Tavria', 125, NULL, NULL),
('Tazzari', 126, 17577, 8695),
('Tesla', 127, 19524, 238),
('Toyota', 128, 44, 239),
('Trabant', 129, 21506, NULL),
('Triumph', 130, 124, 240),
('TVR', 131, NULL, 241),
('UAZ', 132, 115, 8759),
('Vauxhall', 133, 15983, 242),
('Volkswagen', 134, 43, 243),
('Volvo', 135, 42, 244),
('Warszawa', 136, NULL, NULL),
('Wartburg', 137, 118, NULL),
('Weismann', 138, NULL, NULL),
('Yugo', 139, NULL, NULL),
('Zastava', 140, NULL, NULL),
('ZAZ', 141, 113, 8680),
('Zuk', 142, NULL, NULL),
('Kita', 143, 106, NULL),
('AMC', 144, 121, NULL),
('Aston Martin', 145, 100, 141),
('Austin Rover', 146, 15642, NULL),
('Austin-Healey', 147, 27791, NULL),
('Bolloré', 148, 29863, NULL),
('Cobra', 150, 19829, NULL),
('Cupra', 151, 28897, NULL),
('Datsun', 152, 16088, NULL),
('De Lorean', 153, 18736, NULL),
('Desoto', 154, 19741, NULL),
('DR Motor', 155, 16572, NULL),
('DS Automobiles', 156, 29763, NULL),
('Geo', 157, 117, NULL),
('Great Wall', 158, 122, 167),
('Hudson', 159, 27783, NULL),
('International', 160, 13507, NULL),
('JAC', 161, 30005, NULL),
('Land Rover', 162, 73, NULL),
('Norster', 163, 16543, NULL),
('Packard', 164, 18607, NULL),
('Roosevelt', 165, 13514, NULL),
('Secma', 166, 16546, NULL),
('Spartan', 167, 19699, NULL),
('Spyker', 168, 17593, 231),
('Studebaker', 169, 19711, NULL),
('Tartan', 170, 24569, NULL),
('Think', 171, 24720, NULL),
('Venturi', 172, 17380, NULL),
('Wanderer', 173, 10871, NULL),
('Zimmer', 174, 28623, NULL),
('Abarth', 175, NULL, 135),
('Ariel', 176, NULL, 140),
('Auburn', 177, NULL, 142),
('Bristol', 178, NULL, 147),
('Chesil', 179, NULL, 152),
('Corvette', 180, NULL, 156),
('Daimler', 181, NULL, 160),
('Dax', 182, NULL, 161),
('HMC', 183, NULL, 168),
('Humber', 184, NULL, 170),
('Jensen', 185, NULL, 177),
('Locust', 186, NULL, 186),
('MG Motor Uk', 187, NULL, 195),
('MNR', 188, NULL, 199),
('Morris', 189, NULL, 201),
('Noble', 190, NULL, 203),
('Pagani', 191, NULL, 206),
('Panther', 192, NULL, 207),
('Perodua', 193, NULL, 208),
('Pilgrim', 194, NULL, 210),
('Quantum', 195, NULL, 215),
('Radical', 196, NULL, 216),
('Reliant', 197, NULL, 217),
('Reva', 198, NULL, 219),
('Reynard', 199, NULL, 220),
('Riley', 200, NULL, 221),
('Robin Hood', 201, NULL, 222),
('Standard', 202, NULL, 233),
('Volga', 203, NULL, 8976),
('Westfield', 204, NULL, 245);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `car_make`
--
ALTER TABLE `car_make`
  ADD PRIMARY KEY (`car_id`,`make_id`),
  ADD KEY `make_id` (`make_id`);

--
-- Indexes for table `car_queries`
--
ALTER TABLE `car_queries`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `makes`
--
ALTER TABLE `makes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `make` (`make`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `car_queries`
--
ALTER TABLE `car_queries`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
--
-- AUTO_INCREMENT for table `makes`
--
ALTER TABLE `makes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=205;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `car_make`
--
ALTER TABLE `car_make`
  ADD CONSTRAINT `car_make_ibfk_1` FOREIGN KEY (`car_id`) REFERENCES `car_queries` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `car_make_ibfk_2` FOREIGN KEY (`make_id`) REFERENCES `makes` (`id`) ON DELETE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
