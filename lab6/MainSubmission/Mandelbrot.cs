/*using System.Collections;
using System.Collections.Generic;*/
using UnityEngine;

namespace Lab6.Scripts
{
    public class Mandelbrot : MonoBehaviour
    {
        // declare fields (see the Reset method for the required fields)
        [SerializeField] private ComputeShader computeShader;
        [SerializeField] private RenderTexture renderTexture;
        [SerializeField] private Texture2D[] textures;
        [SerializeField] private int iterations;
        [SerializeField] private int bailout;
        [SerializeField] private float bottom;
        [SerializeField] private float left;
        [SerializeField] private float right;
        [SerializeField] private float top;

        private float width;  // calculated by the difference right - left
        private float height;  // calculated by the difference top - bottom
        private int gradientTextureIndex;  // index for determining which color gradient is used

        // Start is called before the first frame update
        void Start()
        {
            renderTexture.enableRandomWrite = true;
            renderTexture.Create();

            iterations = 200;
            bailout = 2;
            left = -2.5f;
            right = 1f;
            bottom = -1f;
            top = 1f;
            width = right - left;
            height = top - bottom;
            gradientTextureIndex = 0;

            // set shader variables (ints and floats)
            computeShader.SetFloat("_Left", left);
            computeShader.SetFloat("_Right", right);
            computeShader.SetFloat("_Bottom", bottom);
            computeShader.SetFloat("_Top", top);
            computeShader.SetInt("_Iterations", iterations);
            computeShader.SetInt("_Bailout", bailout);
            computeShader.SetInt("_Width", renderTexture.width);
            computeShader.SetInt("_Height", renderTexture.height);

            var kernelIndex = computeShader.FindKernel("CSMain");
            computeShader.SetTexture(kernelIndex, "_ColorGradient", textures[gradientTextureIndex]);
            computeShader.SetTexture(kernelIndex, "_MandelbrotSet", renderTexture);
            computeShader.Dispatch(kernelIndex, renderTexture.width / 8, renderTexture.height / 8, 1);
        }

        private void OnDestroy()
        {
            renderTexture.Release();
        }

        private void Reset()
        {
            iterations = 200;
            bailout = 2;
            left = -2.5f;
            right = 1f;
            bottom = -1f;
            top = 1f;
            width = right - left;
            height = top - bottom;
            gradientTextureIndex = 0;

            computeShader.SetFloat("_Left", left);
            computeShader.SetFloat("_Right", right);
            computeShader.SetFloat("_Bottom", bottom);
            computeShader.SetFloat("_Top", top);
            computeShader.SetInt("_Iterations", iterations);
            computeShader.SetInt("_Bailout", bailout);

            var kernelIndex = computeShader.FindKernel("CSMain");
            computeShader.Dispatch(kernelIndex, renderTexture.width / 8, renderTexture.height / 8, 1);
        }

        // Update is called once per frame
        void Update()
        {
            // Reset
            if (Input.GetKeyDown(KeyCode.R))
            {
                Reset();
            }


            Vector2 scale = new Vector2(1f, 1f) * .001f;  // zoom and move speed factor
            // Change of center position via WASD-keys
            if (Input.GetKey(KeyCode.A)) left += -width * scale.x;
            if (Input.GetKey(KeyCode.D)) left += width * scale.x;
            if (Input.GetKey(KeyCode.S)) bottom += -height * scale.y;
            if (Input.GetKey(KeyCode.W)) bottom += height * scale.y;
            right = left + width;
            top = bottom + height;

            // zoom via KeyPad + and -
            float centerX = left + width / 2;
            float centerY = bottom + height / 2;
            if (Input.GetKey(KeyCode.KeypadPlus) || Input.GetKey(KeyCode.Plus))
            {
                width *= 1 - scale.x;
                height *= 1 - scale.y;
            }
            if (Input.GetKey(KeyCode.KeypadMinus) || Input.GetKey(KeyCode.Minus))
            {
                width *= 1 + scale.x;
                height *= 1 + scale.y;
            }
            // zoom with center of new width and height
            left = centerX - width / 2;
            right = centerX + width / 2;
            bottom = centerY - height / 2;
            top = centerY + height / 2;


            // change the colorgradient-texture
            if (Input.GetKeyDown(KeyCode.Space))
            {
                gradientTextureIndex += 1;
                if (gradientTextureIndex >= textures.Length)
                    gradientTextureIndex = 0;
            }

            computeShader.SetFloat("_Left", left);
            computeShader.SetFloat("_Right", right);
            computeShader.SetFloat("_Bottom", bottom);
            computeShader.SetFloat("_Top", top);
            computeShader.SetInt("_Iterations", iterations);
            computeShader.SetInt("_Bailout", bailout);

            var kernelIndex = computeShader.FindKernel("CSMain");
            computeShader.SetTexture(kernelIndex, "_ColorGradient", textures[gradientTextureIndex]);
            computeShader.Dispatch(kernelIndex, renderTexture.width / 8, renderTexture.height / 8, 1);
        }
    }
}

