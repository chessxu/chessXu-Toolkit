import numpy as np
from scipy.io import wavfile
import argparse


def generate_sine_wave(freq, sample_rate, duration, amplitude=0.5):
    """
    生成正弦波

    参数:
        freq: 频率(Hz)
        sample_rate: 采样率(Hz)
        duration: 持续时间(秒)
        amplitude: 振幅(0.0到1.0)

    返回:
        numpy数组包含音频样本
    """
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    return wave


def generate_square_wave(freq, sample_rate, duration, amplitude=0.5):
    """
    生成方波

    参数:
        同上
    """
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * np.sign(np.sin(2 * np.pi * freq * t))
    return wave


def generate_sawtooth_wave(freq, sample_rate, duration, amplitude=0.5):
    """
    生成锯齿波

    参数:
        同上
    """
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * (2 * (t * freq - np.floor(0.5 + t * freq)))
    return wave


def generate_white_noise(sample_rate, duration, amplitude=0.5):
    """
    生成白噪声

    参数:
        同上
    """
    samples = int(sample_rate * duration)
    wave = amplitude * np.random.uniform(-1, 1, samples)
    return wave


def save_wav_file(filename, wave, sample_rate, bit_depth=16):
    """
    保存为WAV文件

    参数:
        filename: 输出文件名
        wave: 音频数据(-1.0到1.0)
        sample_rate: 采样率
        bit_depth: 位深度(16或24)
    """
    # 归一化到适合的整数范围
    if bit_depth == 16:
        wave_normalized = np.int16(wave * 32767)
    elif bit_depth == 24:
        wave_normalized = np.int32(wave * 8388607)
    else:
        raise ValueError("不支持的位深度，请使用16或24")

    wavfile.write(filename, sample_rate, wave_normalized)


def main():
    parser = argparse.ArgumentParser(description='生成指定采样率的音频文件')
    parser.add_argument('filename', type=str, help='输出文件名(.wav)')
    parser.add_argument('--freq', type=float, default=440.0, help='频率(Hz)，默认为440Hz(A4音)')
    parser.add_argument('--sr', type=int, default=44100, help='采样率(Hz)，默认为44100Hz')
    parser.add_argument('--duration', type=float, default=5.0, help='持续时间(秒)，默认为5秒')
    parser.add_argument('--amplitude', type=float, default=0.5, help='振幅(0.0-1.0)，默认为0.5')
    parser.add_argument('--wave', type=str, default='sine',
                        choices=['sine', 'square', 'sawtooth', 'noise'],
                        help='波形类型: sine(默认), square, sawtooth, noise')
    parser.add_argument('--bit', type=int, default=16, choices=[16, 24],
                        help='位深度: 16(默认)或24')

    args = parser.parse_args()

    # 根据选择的波形类型生成相应的波形
    if args.wave == 'sine':
        wave = generate_sine_wave(args.freq, args.sr, args.duration, args.amplitude)
    elif args.wave == 'square':
        wave = generate_square_wave(args.freq, args.sr, args.duration, args.amplitude)
    elif args.wave == 'sawtooth':
        wave = generate_sawtooth_wave(args.freq, args.sr, args.duration, args.amplitude)
    elif args.wave == 'noise':
        wave = generate_white_noise(args.sr, args.duration, args.amplitude)

    # 保存为WAV文件
    save_wav_file(args.filename, wave, args.sr, args.bit)
    print(f"成功生成音频文件: {args.filename}")
    print(
        f"参数: 频率={args.freq}Hz, 采样率={args.sr}Hz, 时长={args.duration}秒, 波形={args.wave}, 位深度={args.bit}bit")


if __name__ == "__main__":
    main()