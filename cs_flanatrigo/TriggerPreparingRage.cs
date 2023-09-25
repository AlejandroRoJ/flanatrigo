using System.Timers;

namespace CSFlanaTrigo
{
    internal class TriggerPreparingRage : TriggerRage
    {
        private readonly TriggerNormal _triggerNormal;
        private Timer _timer;

        public TriggerPreparingRage(Wrapper wrapper) : base(wrapper)
        {
            _triggerNormal = new TriggerNormal(wrapper);
            _timer = new Timer()
            {
                AutoReset = false
            };
            _timer.Elapsed += OnTimeElapsed;

            wrapper.OnRageImmobilityChanged += OnRageImmobilityChanged;
            //wrapper.OnRestartRageTimer += OnRestartRageTimer;
        }

        public override bool ColorSearch(int x, int y, int offset, byte blue, byte green, byte red)
        {
            bool result = _triggerNormal.ColorSearch(x, y, offset, blue, green, red)
                          ||
                          base.ColorSearch(x, y, offset, blue, green, red);
            if (result)
            {
                StartTimer();
            }
            return result;
        }

        public override void StartTimer()
        {
            StopTimer();
            OnStopDetectEnemy();
            OnStartDetectEnemy();
            _timer.Start();
        }

        public override void StopTimer()
        {
            _timer.Stop();
        }

        private void OnRageImmobilityChanged(int rageImmobility)
        {
            if (rageImmobility > 0)
            {
                _timer.Interval = rageImmobility;
            }

            if (_timer.Enabled)
            {
                if (rageImmobility == 0)
                {
                    OnTimeElapsed();
                }
                else
                {
                    StartTimer();
                }
            }
        }

        private void OnRestartRageTimer()
        {
            _wrapper.TriggerMode = TriggerMode.PreparingRage;
            StartTimer();
        }

        private void OnTimeElapsed(object source = null, System.Timers.ElapsedEventArgs e = null)
        {
            _wrapper.TriggerMode = TriggerMode.Rage;
        }
    }
}
