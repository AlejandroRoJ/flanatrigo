using System.Drawing;
using System.Drawing.Imaging;

namespace CSFlanaTrigo
{
    public class ScreenCapturer
    {
        private const PixelFormat PIXEL_FORMAT = PixelFormat.Format24bppRgb;

        public static Bitmap CaptureRegion(int x, int y, int width, int height)
        {
            Bitmap bitmap = new Bitmap(width, height, PIXEL_FORMAT);
            using Graphics graphics = Graphics.FromImage(bitmap);
            graphics.CopyFromScreen(x, y, 0, 0, bitmap.Size);

            return bitmap;
        }

        public static BitmapData LockBitmap(Bitmap bitmap)
        {
            Rectangle captureBounds = new Rectangle(Point.Empty, bitmap.Size);

            return bitmap.LockBits(captureBounds, ImageLockMode.ReadOnly, bitmap.PixelFormat);
        }
    }
}
