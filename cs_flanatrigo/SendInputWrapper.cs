using System;
using System.Runtime.InteropServices;

namespace CSFlanaTrigo
{
    [StructLayout(LayoutKind.Sequential)]
    public struct KeyboardInput
    {
        public ushort wVk;
        public ushort wScan;
        public uint dwFlags;
        public uint time;
        public IntPtr dwExtraInfo;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct MouseInput
    {
        public int dx;
        public int dy;
        public uint mouseData;
        public uint dwFlags;
        public uint time;
        public IntPtr dwExtraInfo;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct HardwareInput
    {
        public uint uMsg;
        public ushort wParamL;
        public ushort wParamH;
    }

    [StructLayout(LayoutKind.Explicit)]
    public struct InputUnion
    {
        [FieldOffset(0)] public MouseInput mi;
        [FieldOffset(0)] public KeyboardInput ki;
        [FieldOffset(0)] public HardwareInput hi;
    }

    public struct Input
    {
        public int type;
        public InputUnion u;
    }

    [Flags]
    public enum InputType
    {
        Mouse = 0,
        Keyboard = 1,
        Hardware = 2
    }

    [Flags]
    public enum KeyEventF
    {
        KeyDown = 0x0000,
        ExtendedKey = 0x0001,
        KeyUp = 0x0002,
        Unicode = 0x0004,
        Scancode = 0x0008
    }

    [Flags]
    public enum MouseEventF
    {
        Absolute = 0x8000,
        HWheel = 0x01000,
        Move = 0x0001,
        MoveNoCoalesce = 0x2000,
        LeftDown = 0x0002,
        LeftUp = 0x0004,
        RightDown = 0x0008,
        RightUp = 0x0010,
        MiddleDown = 0x0020,
        MiddleUp = 0x0040,
        VirtualDesk = 0x4000,
        Wheel = 0x0800,
        XDown = 0x0080,
        XUp = 0x0100
    }

    public class InputEvent
    {
        public Input[] Presses { get; private set; }
        public Input[] Releases { get; private set; }
        public uint Length { get; private set; }

        public InputEvent(Input[] presses, Input[] releases)
        {
            Presses = presses;
            Releases = releases;
            Length = (uint)Presses.Length;
        }
    }

    public class SendInputWrapper
    {
        private static readonly int inputSize = Marshal.SizeOf(typeof(Input));

        [DllImport("user32.dll")]
        public static extern IntPtr GetMessageExtraInfo();

        [DllImport("user32.dll", SetLastError = true)]
        public static extern uint SendInput(uint nInputs, Input[] pInputs, int cbSize);

        public static uint SendInput(uint nInputs, Input[] pInputs)
        {
            return SendInput(nInputs, pInputs, inputSize);
        }

        public static InputEvent getKeyboardInputs(int[] scanCodes)
        {
            Input[] presses = new Input[scanCodes.Length];
            Input[] releases = new Input[scanCodes.Length];

            for (int i = 0; i < scanCodes.Length; i++)
            {
                presses[i] = new Input
                {
                    type = (int)InputType.Keyboard,
                    u = new InputUnion
                    {
                        ki = new KeyboardInput
                        {
                            wVk = 0,
                            wScan = (ushort)scanCodes[i],
                            dwFlags = (uint)(KeyEventF.KeyDown | KeyEventF.Scancode),
                            dwExtraInfo = SendInputWrapper.GetMessageExtraInfo()
                        }
                    }
                };
                releases[i] = new Input
                {
                    type = (int)InputType.Keyboard,
                    u = new InputUnion
                    {
                        ki = new KeyboardInput
                        {
                            wVk = 0,
                            wScan = (ushort)scanCodes[i],
                            dwFlags = (uint)(KeyEventF.KeyUp | KeyEventF.Scancode),
                            dwExtraInfo = SendInputWrapper.GetMessageExtraInfo()
                        }
                    }
                };
            }

            return new InputEvent(presses, releases);
        }

        public static InputEvent getMouseInputs(string[] buttonNames)
        {
            Input[] presses = new Input[buttonNames.Length];
            Input[] releases = new Input[buttonNames.Length];

            for (int i = 0; i < buttonNames.Length; i++)
            {
                uint dwFlagsPress;
                uint dwFlagsRelease;
                uint mouseData;
                switch (buttonNames[i])
                {
                    case "left":
                        mouseData = 0;
                        dwFlagsPress = (uint)MouseEventF.LeftDown;
                        dwFlagsRelease = (uint)MouseEventF.LeftUp;
                        break;
                    case "right":
                        mouseData = 0;
                        dwFlagsPress = (uint)MouseEventF.RightDown;
                        dwFlagsRelease = (uint)MouseEventF.RightUp;
                        break;
                    case "middle":
                        mouseData = 0;
                        dwFlagsPress = (uint)MouseEventF.MiddleDown;
                        dwFlagsRelease = (uint)MouseEventF.MiddleUp;
                        break;
                    case "x":
                        mouseData = 0x0001;
                        dwFlagsPress = (uint)MouseEventF.XDown;
                        dwFlagsRelease = (uint)MouseEventF.XUp;
                        break;
                    case "x2":
                        mouseData = 0x0002;
                        dwFlagsPress = (uint)MouseEventF.XDown;
                        dwFlagsRelease = (uint)MouseEventF.XUp;
                        break;
                    default:
                        continue;

                }
                presses[i] = new Input
                {
                    type = (int)InputType.Mouse,
                    u = new InputUnion
                    {
                        mi = new MouseInput
                        {
                            mouseData = mouseData,
                            dwFlags = dwFlagsPress,
                            dwExtraInfo = SendInputWrapper.GetMessageExtraInfo()
                        }
                    }
                };
                releases[i] = new Input
                {
                    type = (int)InputType.Mouse,
                    u = new InputUnion
                    {
                        mi = new MouseInput
                        {
                            mouseData = mouseData,
                            dwFlags = dwFlagsRelease,
                            dwExtraInfo = SendInputWrapper.GetMessageExtraInfo()
                        }
                    }
                };
            }

            return new InputEvent(presses, releases);
        }
    }
}
