using System.IO.Ports;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;

namespace GUI_csharp
{
    /// <summary>
    ///     By default, for Servos like MG996R the range 0-180 is set,
    ///     well if something will interfere with the servo rotation -
    ///     it is very bad, so you will need to calibrate the range of
    ///     rotation manually.
    ///     This must be done in the function SetRangeServo
    /// </summary>
 
    public partial class MainWindow : Window
    {
        private SerialPort _serialPort;
        private bool _connected;
        private List<Slider> _sliders;

        public MainWindow()
        {
            InitializeComponent();
            _serialPort = new SerialPort
            {
                BaudRate = 115200
            };
            foreach (string port in SerialPort.GetPortNames())
            {
                listComPorts.Items.Add(port);
            }
            _sliders = new List<Slider>{ servo0, servo1, servo2, servo3, servo4, servo5 };
            SetupConnections();
            SetRangeServo();
            UpdateServoState();
        }
        private void SetupConnections()
        {
            for (int i = 0; i < _sliders.Count; i++)
            {
                int numEngine = i;
                _sliders[numEngine].ValueChanged += (sender, e) => OnServo((int)_sliders[numEngine].Value, numEngine);
            }
        }
        private void OnServo(int val, int numEngine)
        {
            if (_serialPort.IsOpen)
            {
                string outputData = $"{numEngine}:{val}";
                _serialPort.Write($"{outputData}\n");
                UpdateStatus($"send data: {outputData}");
            }

        }
        private void SetRangeServo()
        {
            servo0.Minimum = 24;
            servo0.Maximum = 97;
            servo1.Minimum = 0;
            servo1.Maximum = 180;
            servo2.Minimum = 0;
            servo2.Maximum = 180;
            servo3.Minimum = 0;
            servo3.Maximum = 180;
            servo4.Minimum = 0;
            servo4.Maximum = 180;
            servo5.Minimum = 0;
            servo5.Maximum = 180;
        }
        private void UpdateServoState()
        {
            foreach (Slider slider in _sliders)
                slider.IsEnabled = _connected;
        }

        private void btnOpenComPort_Click(object sender, RoutedEventArgs e)
        {
            _serialPort.PortName = listComPorts.SelectedItem.ToString();
            try
            {
                _serialPort.Open();
                _connected = true;
                UpdateStatus($"Opened {_serialPort.PortName}");
            }
            catch (Exception)
            {
                _connected = false;
                UpdateStatus($"Failed to open {_serialPort.PortName}");
            }
            UpdateServoState();
        }

        private void btnCloseComPort_Click(object sender, RoutedEventArgs e)
        {
            if (_serialPort.IsOpen)
            {
                _serialPort.Close();
                _connected = false;
                UpdateStatus("COM port Arduino: closed");
            }
            UpdateServoState();
        }

        private void UpdateStatus(string message)
        {
            StatusBarInfo.Text = message;
        }

        protected override void OnClosed(EventArgs e)
        {
            if (_serialPort.IsOpen)
            {
                _serialPort.Close();
            }
            base.OnClosed(e);
        }


    }
}