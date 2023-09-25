namespace CSFlanaTrigo
{
    public struct Range
    {
        public int Min { get; set; }
        public int Max { get; set; }

        public Range(int min, int max)
        {
            Min = min;
            Max = max;
        }

        public bool IsInRange(int value)
        {
            return Min <= value && value <= Max;
        }
    }
}
