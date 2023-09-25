using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace CSFlanaTrigo
{
    internal abstract class TriggerBase
    {
        protected const int BYTES_PER_PIXEL = 3;
        protected StringBuilder? _debugBuilder;
        protected Func<BitmapData, bool>? _pixelSearchFunc;
        protected Func<int, int, int, byte, byte, byte, bool>? _colorSearchFunc;
        protected readonly Wrapper _wrapper;
        protected readonly Mouse _mouse;


        public TriggerBase(Wrapper wrapper)
        {
            _wrapper = wrapper;
            _mouse = new Mouse(_wrapper);

            _wrapper.OnTestModeChanged += OnTestModeChanged;
            OnTestModeChanged(TestMode.None);
        }

        public abstract bool ColorSearch(int x, int y, int offset, byte blue, byte green, byte red);

        public void DetectEnemy()
        {
            using Bitmap bitmap = ScreenCapturer.CaptureRegion(
                    _wrapper.DetectorX,
                    _wrapper.DetectorY,
                    _wrapper.DetectorSize,
                    _wrapper.DetectorSize
                );
            BitmapData bitmapData = ScreenCapturer.LockBitmap(bitmap);

            if (_pixelSearchFunc(bitmapData))
            {
                OnEnemyDetected();
            }

            bitmap.UnlockBits(bitmapData);
        }

        public virtual void OnStartDetectEnemy()
        {
        }

        public virtual void OnStopDetectEnemy()
        {
        }

        public virtual void StartTimer()
        {
        }

        public virtual void StopTimer()
        {
        }

        private bool ConsoleColorSearch(int x, int y, int offset, byte blue, byte green, byte red)
        {
            if (x == 0 && y != 0)
            {
                _debugBuilder.AppendLine();
            }
            if (ColorSearch(x, y, offset, blue, green, red))
            {
                _debugBuilder.Append("o  ");
            }
            else
            {
                _debugBuilder.Append("'  ");
            }

            return false;
        }

        private bool ConsolePixelSearch(BitmapData bitmapData)
        {
            _debugBuilder = new StringBuilder();
            _debugBuilder.AppendLine($"Trigger: {_wrapper.TriggerMode} | Task id: {Task.CurrentId}");
            bool result = PixelSearch(bitmapData);
            _debugBuilder.AppendLine();
            Console.WriteLine(_debugBuilder);
            Thread.Sleep(_wrapper.ConsoleModeSleep);
            return result;
        }

        private void OnEnemyDetected()
        {
            switch (_wrapper.TestMode)
            {
                case TestMode.None:
                    _mouse.Click();
                    break;
                case TestMode.Beep:
                    Console.Beep(1000, 100);
                    break;
            }
        }

        private void OnTestModeChanged(TestMode testMode)
        {
            switch (testMode)
            {
                case TestMode.None:
                case TestMode.Beep:
                    _pixelSearchFunc = PixelSearch;
                    _colorSearchFunc = ColorSearch;
                    break;
                case TestMode.Console:
                    _pixelSearchFunc = ConsolePixelSearch;
                    _colorSearchFunc = ConsoleColorSearch;
                    break;
            }
        }

        private bool PixelSearch(BitmapData bitmapData)
        {
            unsafe
            {
                int stride = bitmapData.Stride;
                byte* ptr = (byte*)bitmapData.Scan0;

                for (int y = 0; y < bitmapData.Height; y++)
                {
                    for (int x = 0; x < bitmapData.Width; x++)
                    {
                        int offset = y * stride + x * BYTES_PER_PIXEL;
                        if (_colorSearchFunc(x, y, offset, ptr[offset], ptr[offset + 1], ptr[offset + 2]))
                            return true;
                    }
                }
            }
            return false;
        }
    }
}
