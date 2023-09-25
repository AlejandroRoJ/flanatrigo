using System;
using System.Drawing;
using System.Drawing.Imaging;

namespace CSFlanaTrigo
{
    unsafe internal class TriggerRage : TriggerBase
    {
        protected Bitmap _previousBitmap;
        protected BitmapData _previousBitmapData;
        protected byte* _previousPtr;
        protected bool areBitsLocked = false;

        public TriggerRage(Wrapper wrapper) : base(wrapper)
        {
        }

        public override bool ColorSearch(int x, int y, int offset, byte blue, byte green, byte red)
        {
            return Math.Abs(blue - _previousPtr[offset]) > _wrapper.RageTolerance
                   ||
                   Math.Abs(green - _previousPtr[offset + 1]) > _wrapper.RageTolerance
                   ||
                   Math.Abs(red - _previousPtr[offset + 2]) > _wrapper.RageTolerance;
        }

        public override void OnStartDetectEnemy()
        {
            _previousBitmap = ScreenCapturer.CaptureRegion(
                    _wrapper.DetectorX,
                    _wrapper.DetectorY,
                    _wrapper.DetectorSize,
                    _wrapper.DetectorSize
                );
            _previousBitmapData = ScreenCapturer.LockBitmap(_previousBitmap);
            _previousPtr = (byte*)_previousBitmapData.Scan0;
            areBitsLocked = true;
        }

        public override void OnStopDetectEnemy()
        {
            if (!areBitsLocked)
            {
                return;
            }

            try
            {
                _previousBitmap.UnlockBits(_previousBitmapData);
                _previousBitmap.Dispose();
                areBitsLocked = false;
            }
            catch (System.InvalidOperationException)
            {
            }
        }
    }
}
