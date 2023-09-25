namespace CSFlanaTrigo
{
    internal class TriggerNormal : TriggerBase
    {
        public TriggerNormal(Wrapper wrapper) : base(wrapper)
        {
        }

        public override bool ColorSearch(int x, int y, int offset, byte blue, byte green, byte red)
        {
            return _wrapper.BlueRange.IsInRange(blue)
                   &&
                   _wrapper.GreenRange.IsInRange(green)
                   &&
                   _wrapper.RedRange.IsInRange(red);
        }
    }
}
