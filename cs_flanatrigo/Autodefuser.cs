using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

namespace CSFlanaTrigo
{
    public class Autodefuser
    {
        private const int BYTES_PER_PIXEL = 3;
        private CancellationTokenSource? _cancellationTokenSource;
        private readonly Wrapper _wrapper;
        private readonly Mouse _mouse;
        private InputEvent _keyboardInputs;
        private InputEvent _mouseInputs;

        public Autodefuser(Wrapper wrapper)
        {
            _wrapper = wrapper;
            _mouse = new Mouse(wrapper);

            _wrapper.OnDefuserKeyboardScanCodesChanged += OnDefuserKeyboardScanCodesChanged;
            _wrapper.OnDefuserMouseButtonNamesChanged += OnDefuserMouseButtonNamesChanged;
        }

        public void Start()
        {
            if (_cancellationTokenSource is null || _cancellationTokenSource.IsCancellationRequested)
            {
                _cancellationTokenSource = new CancellationTokenSource();
                Task.Run(() => SearchBomb(_cancellationTokenSource.Token));
            }
        }

        public void Stop()
        {
            _cancellationTokenSource?.Cancel();
        }

        private void Defuse(CancellationToken cancellationToken)
        {
            Thread.Sleep(Math.Max(0, _wrapper.DefuserBombDuration - _wrapper.DefuseSeconds - _wrapper.DefuserAdvance));
            if (!cancellationToken.IsCancellationRequested)
            {
                PressKeyboardButtons();
                PressMouseButtons();
                Thread.Sleep(_wrapper.DefuseSeconds + _wrapper.DefuseSecondsExtra);
                ReleaseKeyboardButtons();
                ReleaseMouseButtons();
            }
        }

        private bool IsColorInRegion(int[] region, Color[] targetColors, int tolerance)
        {
            using Bitmap bitmap = ScreenCapturer.CaptureRegion(region[0], region[1], region[2] - region[0], region[3] - region[1]);
            BitmapData bitmapData = ScreenCapturer.LockBitmap(bitmap);
            unsafe
            {
                int stride = bitmapData.Stride;
                byte* ptr = (byte*)bitmapData.Scan0;

                for (int y = 0; y < bitmapData.Height; y++)
                {
                    for (int x = 0; x < bitmapData.Width; x++)
                    {
                        int offset = y * stride + x * BYTES_PER_PIXEL;

                        if (
                            targetColors.Any(
                                targetColor =>
                                    Math.Abs(targetColor.B - ptr[offset]) <= tolerance
                                    &&
                                    Math.Abs(targetColor.G - ptr[offset + 1]) <= tolerance
                                    &&
                                    Math.Abs(targetColor.R - ptr[offset + 2]) <= tolerance
                            )
                        )
                        {
                            return true;
                        }
                    }
                }
            }
            return false;
        }

        private bool IsRegionColor(int[] region, Color[] targetColors, int tolerance)
        {
            Color color = RegionColorMean(region);
            return targetColors.Any(
                targetColor =>
                    Math.Abs(targetColor.B - color.B) <= tolerance
                    &&
                    Math.Abs(targetColor.G - color.G) <= tolerance
                    &&
                    Math.Abs(targetColor.R - color.R) <= tolerance
            );
        }

        private void OnDefuserKeyboardScanCodesChanged(int[] scanCodes)
        {
            _keyboardInputs = SendInputWrapper.getKeyboardInputs(scanCodes);
        }

        private void OnDefuserMouseButtonNamesChanged(string[] buttonNames)
        {
            _mouseInputs = SendInputWrapper.getMouseInputs(buttonNames);
        }

        private void PressKeyboardButtons()
        {
            if (_keyboardInputs != null)
            {
                SendInputWrapper.SendInput(_keyboardInputs.Length, _keyboardInputs.Presses);
            }
        }

        private void PressMouseButtons()
        {
            if (_mouseInputs != null)
            {
                SendInputWrapper.SendInput(_mouseInputs.Length, _mouseInputs.Presses);
            }
        }

        private void ReleaseKeyboardButtons()
        {
            if (_keyboardInputs != null)
            {
                SendInputWrapper.SendInput(_keyboardInputs.Length, _keyboardInputs.Releases);
            }
        }

        private void ReleaseMouseButtons()
        {
            if (_mouseInputs != null)
            {
                SendInputWrapper.SendInput(_mouseInputs.Length, _mouseInputs.Releases);
            }
        }

        private Color RegionColorMean(int[] region)
        {
            using Bitmap bitmap = ScreenCapturer.CaptureRegion(region[0], region[1], region[2] - region[0], region[3] - region[1]);
            BitmapData bitmapData = ScreenCapturer.LockBitmap(bitmap);
            int blue_sum = 0;
            int green_sum = 0;
            int red_sum = 0;
            int n_pixels = bitmapData.Width * bitmapData.Height;
            unsafe
            {
                int stride = bitmapData.Stride;
                byte* ptr = (byte*)bitmapData.Scan0;

                for (int y = 0; y < bitmapData.Height; y++)
                {
                    for (int x = 0; x < bitmapData.Width; x++)
                    {
                        int offset = y * stride + x * BYTES_PER_PIXEL;

                        blue_sum += (int)Math.Pow(ptr[offset], 2);
                        green_sum += (int)Math.Pow(ptr[offset + 1], 2);
                        red_sum += (int)Math.Pow(ptr[offset + 2], 2);
                    }
                }
            }
            return Color.FromArgb(
                    (int)Math.Sqrt(red_sum / n_pixels),
                    (int)Math.Sqrt(green_sum / n_pixels),
                    (int)Math.Sqrt(blue_sum / n_pixels)
                );
        }

        private void SearchBomb(CancellationToken cancellationToken)
        {
            while (!cancellationToken.IsCancellationRequested)
            {
                while (
                    IsColorInRegion(_wrapper.DefuserPointARegion, _wrapper.DefuserPointsColors, _wrapper.DefuserPointsColorTolerance)
                    ||
                    IsColorInRegion(_wrapper.DefuserPointBRegion, _wrapper.DefuserPointsColors, _wrapper.DefuserPointsColorTolerance)
                    ||
                    !IsColorInRegion(_wrapper.DefuserBombRegion, _wrapper.DefuserBombColors, _wrapper.DefuserBombColorTolerance)
                    )
                {
                    if (cancellationToken.IsCancellationRequested)
                    {
                        return;
                    }
                }
                Defuse(cancellationToken);
            }
        }
    }
}
