# Driver Drowsiness Detection System 

A real-time computer vision–based system that detects driver drowsiness using eye aspect ratio (EAR) analysis and provides alerts to improve road safety. The system includes a live monitoring module and a data visualization dashboard.

---

## 📌 Project Overview

This project monitors a driver’s eye movements using a webcam and detects signs of drowsiness in real time. When prolonged eye closure is detected, an alert is triggered. The collected data is logged and visualized using an interactive dashboard.

The system aims to reduce accident risks caused by fatigue and inattentiveness.

---

## ⚙️ Features

- Real-time face and eye tracking using MediaPipe  
- Eye Aspect Ratio (EAR) calculation  
- Drowsiness detection based on threshold values  
- Sound alert on drowsiness detection  
- Automatic logging of eye data and status  
- Interactive dashboard for analysis  
- Data visualization using R Shiny  

---

## Technology Stack

### Programming Languages
- Python  
- R  

### Libraries & Frameworks
- OpenCV  
- MediaPipe  
- NumPy  
- Shiny (R)  
- ggplot2  
- dplyr  

### Tools
- Git & GitHub  
- Webcam  
- RStudio  
- VS Code  

---

## Project Structure

```
drowsiness_detection/
│
├── dashboard/
│   └── app.R
│
├── logs/
│   ├── ear_log.csv
│   └── drowsiness_log.csv
│
├── alarm.wav
├── main.py
├── analysis.R
├── requirements.txt
└── README.md
```

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/drowsiness-detection.git
cd drowsiness-detection
```

---

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Run the Detection System

```bash
python main.py
```

This will start the webcam and begin logging data.

---

### 4. Run Data Analysis (Optional)

```bash
Rscript analysis.R
```

---

### 5. Launch Dashboard

Open RStudio and run:

```r
library(shiny)
runApp("dashboard")
```

Then open the browser link displayed in the console.

---

## Output

- Live EAR and drowsiness status display  
- CSV log files stored in `logs/`  
- Visual plots on the dashboard  
- Real-time alerts on fatigue detection  

---

## Methodology

1. Capture video using webcam  
2. Detect facial landmarks using MediaPipe  
3. Extract eye coordinates  
4. Calculate Eye Aspect Ratio (EAR)  
5. Compare with threshold  
6. Trigger alert if drowsy  
7. Store data in CSV logs  
8. Visualize using Shiny dashboard  

---

## Applications

- Driver safety systems  
- Fleet monitoring  
- Smart vehicles  
- Accident prevention systems  
- Fatigue monitoring  

---

## Future Enhancements

- Mobile application integration  
- Machine learning–based prediction  
- Cloud-based analytics  
- Multi-driver support  
- Mobile camera support  

---


## Acknowledgements

- MediaPipe Team  
- OpenCV Community  
- R Shiny Developers  
- Open Source Contributors  
