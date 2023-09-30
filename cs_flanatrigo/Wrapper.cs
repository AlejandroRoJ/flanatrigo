using System;
using System.Drawing;

namespace CSFlanaTrigo
{
    public class Wrapper
    {
        // -----------------------------
        // ---------- Trigger ----------
        // -----------------------------
        public int ClickDelay { get; set; }
        public int DetectorX { get; set; }
        public int DetectorY { get; set; }
        public int DetectorSize { get; set; }
        public Color Color
        {
            get => _color;
            set
            {
                _color = value;
                UpdateRanges();
            }
        }
        public Range BlueRange { get; set; }
        public Range GreenRange { get; set; }
        public Range RedRange { get; set; }
        public int Tolerance
        {
            get => _tolerance;
            set
            {
                _tolerance = value;
                UpdateRanges();
            }
        }
        public TriggerMode TriggerMode { get; set; }
        public int RageImmobility
        {
            get => _rageImmobility;
            set
            {
                if (_rageImmobility != value)
                {
                    _rageImmobility = value;
                    OnRageImmobilityChanged?.Invoke(_rageImmobility);
                }
            }
        }
        public int RageTolerance { get; set; }
        public DebugMode DebugMode
        {
            get => _debugMode;
            set
            {
                if (_debugMode != value)
                {
                    _debugMode = value;
                    OnDebugModeChanged?.Invoke(_debugMode);
                }
            }
        }
        public int ConsoleModeSleep { get; set; }
        public event Action<int>? OnRageImmobilityChanged;
        public event Action<DebugMode>? OnDebugModeChanged;
        private Color _color;
        private int _tolerance;
        private int _rageImmobility;
        private DebugMode _debugMode;

        private void UpdateRanges()
        {
            RedRange = new Range(Color.R - Tolerance, Color.R + Tolerance);
            GreenRange = new Range(Color.G - Tolerance, Color.G + Tolerance);
            BlueRange = new Range(Color.B - Tolerance, Color.B + Tolerance);
        }

        // ---------------------------------
        // ---------- Autodefuser ----------
        // ---------------------------------        
        public int DefuseSeconds { get; set; }
        public int DefuseSecondsExtra { get; set; }
        public int DefuserBombDuration { get; set; }
        public Color[] DefuserColors { get; set; }
        public int DefuserColorTolerance { get; set; }
        public int[] DefuserRegion { get; set; }
        public int[] DefuserKeyboardScanCodes
        {
            get
            {
                return _defuserKeyboardScanCodes;
            }
            set
            {
                _defuserKeyboardScanCodes = value;
                OnDefuserKeyboardScanCodesChanged?.Invoke(value);
            }
        }
        public string[] DefuserMouseButtonNames
        {
            get
            {
                return _defuserMouseButtonNames;
            }
            set
            {
                _defuserMouseButtonNames = value;
                OnDefuserMouseButtonNamesChanged?.Invoke(value);
            }
        }
        public int DefuserAdvance { get; set; }
        public event Action<int[]>? OnDefuserKeyboardScanCodesChanged;
        public event Action<string[]>? OnDefuserMouseButtonNamesChanged;
        private int[] _defuserKeyboardScanCodes;
        private string[] _defuserMouseButtonNames;
    }
}
