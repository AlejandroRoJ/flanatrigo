using System.Threading;

namespace CSFlanaTrigo
{


    public class Mouse
    {
        private readonly Wrapper _wrapper;
        private readonly InputEvent _mouseInputs;

        public Mouse(Wrapper wrapper)
        {
            _wrapper = wrapper;
            _mouseInputs = SendInputWrapper.getMouseInputs(new string[] { "left" });
        }

        public void Click()
        {
            SendInputWrapper.SendInput(_mouseInputs.Length, _mouseInputs.Presses);
            Thread.Sleep(_wrapper.ClickDelay);
            SendInputWrapper.SendInput(_mouseInputs.Length, _mouseInputs.Releases);
        }
    }
}
