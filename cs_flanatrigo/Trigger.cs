using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

namespace CSFlanaTrigo
{
    public class Trigger
    {
        private CancellationTokenSource? _cancellationTokenSource;
        private readonly Dictionary<TriggerMode, TriggerBase> _triggers;
        private readonly Wrapper _wrapper;

        public Trigger(Wrapper wrapper)
        {
            _wrapper = wrapper;
            _triggers = new Dictionary<TriggerMode, TriggerBase>()
            {
                { TriggerMode.Normal, new TriggerNormal(_wrapper) },
                { TriggerMode.PreparingRage, new TriggerPreparingRage(_wrapper) },
                { TriggerMode.Rage, new TriggerRage(_wrapper) }
            };
        }

        private void Run(CancellationToken cancellationToken)
        {
            TriggerBase trigger = _triggers[_wrapper.TriggerMode];
            trigger.StartTimer();
            trigger.OnStartDetectEnemy();
            while (!cancellationToken.IsCancellationRequested)
            {
                trigger.DetectEnemy();
            }
            trigger.OnStopDetectEnemy();
            trigger.StartTimer();
        }

        public void Start()
        {
            if (_cancellationTokenSource is null || _cancellationTokenSource.IsCancellationRequested)
            {
                _cancellationTokenSource = new CancellationTokenSource();
                Task.Run(() => Run(_cancellationTokenSource.Token));
            }
        }

        public void Stop()
        {
            _cancellationTokenSource?.Cancel();
        }
    }
}