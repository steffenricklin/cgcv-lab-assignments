using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Lab6.Scripts
{
    public class Mandelbrot : MonoBehaviour

    {

        [SerializeField] private ComputeShader computeShader;
        [SerializeField] private RenderTexture renderTexture;
        [SerializeField] private Texture texture1;
        [SerializeField] private Texture texture2;
        [SerializeField] private Texture texture3;
        [SerializeField] private Texture texture4;
        [SerializeField] private Texture texture5;
        [SerializeField] private Texture texture6;
        [SerializeField] private float left;
        [SerializeField] private float right;
        [SerializeField] private float top;
        [SerializeField] private float bottom;
        private float width;
        private float hight;
        private float xScale;
        private float yScale;
        [SerializeField] private float iterations;
        [SerializeField] private float bailout;
        [SerializeField] private float speed;
        private int colors;

        private void Start()
        {
            colors = 1;
            // Scale of the current x and y axis 
            xScale = right - left;
            yScale = top - bottom;

            renderTexture.enableRandomWrite = true;
            renderTexture.Create();

            var kernelIndex = computeShader.FindKernel("CSMain");

            // height and width are the pixel length of the image 
            width = GetComponent<RectTransform>().rect.width;
            hight = GetComponent<RectTransform>().rect.height;

            // Set shader variables (ints and floats)
            // Can't use decimal or double here :/ 
            computeShader.SetFloat("_Left", left);
            computeShader.SetFloat("_Right", right);
            computeShader.SetFloat("_Top", top);
            computeShader.SetFloat("_Bottom", bottom);
            computeShader.SetFloat("_Width", width);
            computeShader.SetFloat("_Hight", hight);
            computeShader.SetFloat("_Iterations", iterations);
            computeShader.SetFloat("_Bailout", bailout);

            computeShader.SetTexture(kernelIndex, "_ColorGradient", texture1);
            computeShader.SetTexture(kernelIndex, "_MandelbrotSet", renderTexture);
            computeShader.Dispatch(kernelIndex, renderTexture.width / 8, renderTexture.height / 8, 1);
        }



        // Update is called once per frame
        void Update()
        {

            // Zoom in
            if (Input.GetMouseButtonDown(0))
            {
                // get scaled(0,1) postion of the mouse 
                float prtx = Input.mousePosition.x / width;
                float prty = Input.mousePosition.y / hight;
                // get position of the mouse in the coordinate system 
                float mousePositionx = (prtx * xScale + left);
                float mousePositiony = (prty * yScale + bottom);

                // new center is between this position and the current center
                // to avoid overshooting
                float new_positionx = 0.3f * mousePositionx + 0.7f * ((xScale / 2 + left));
                float new_positiony = 0.3f * mousePositiony + 0.7f * ((yScale / 2 + bottom));

            
                // new zoomed in scale
                float zoomvalueX = xScale * speed;
                float zoomvalueY = yScale * speed;
                // override all old scale
                xScale = xScale - zoomvalueX;
                yScale = yScale - zoomvalueY;
                // calculate border postions around new center
                left = new_positionx - (xScale * 0.6f);
                right = new_positionx + (xScale * 0.4f);
                bottom = new_positiony - (yScale * 0.6f);
                top = new_positiony + (yScale * 0.4f);

                computeShader.SetFloat("_Left", left);
                computeShader.SetFloat("_Right", right);
                computeShader.SetFloat("_Top", top);
                computeShader.SetFloat("_Bottom", bottom);


                var kernelIndex = computeShader.FindKernel("CSMain");
                computeShader.Dispatch(kernelIndex, renderTexture.width / 8, renderTexture.height / 8, 1);
            }


            // zoom out
            if (Input.GetKeyDown("space"))
            {

                // zoom out with double speed
                float zoomvalueX = xScale * speed * 2;
                float zoomvalueY = yScale * speed * 2;
                // get new scale
                xScale = xScale + zoomvalueX;
                yScale = yScale + zoomvalueY;
                left = left - (zoomvalueX * 0.1f);
                right = right + (zoomvalueX * 0.9f);
                bottom = bottom - (zoomvalueY * 0.1f);
                top = top + (zoomvalueY * 0.9f);


                computeShader.SetFloat("_Left", left);
                computeShader.SetFloat("_Right", right);
                computeShader.SetFloat("_Top", top);
                computeShader.SetFloat("_Bottom", bottom);


                var kernelIndex = computeShader.FindKernel("CSMain");
                computeShader.Dispatch(kernelIndex, renderTexture.width / 8, renderTexture.height / 8, 1);


            }

            if (Input.GetKeyDown(KeyCode.M))
            {

                if (colors == 1)
                {
                    var kernelIndex = computeShader.FindKernel("CSMain");
                    computeShader.SetTexture(kernelIndex, "_ColorGradient", texture2);
                    computeShader.Dispatch(kernelIndex, renderTexture.width / 8, renderTexture.height / 8, 1);
                    colors = 2;
                }

                else if (colors == 2)
                {
                    var kernelIndex = computeShader.FindKernel("CSMain");
                    computeShader.SetTexture(kernelIndex, "_ColorGradient", texture3);
                    computeShader.Dispatch(kernelIndex, renderTexture.width / 8, renderTexture.height / 8, 1);
                    colors = 3;
                }

                else if (colors == 3)
                {
                    var kernelIndex = computeShader.FindKernel("CSMain");
                    computeShader.SetTexture(kernelIndex, "_ColorGradient", texture4);
                    computeShader.Dispatch(kernelIndex, renderTexture.width / 8, renderTexture.height / 8, 1);
                    colors = 4;
                }
                else if (colors == 4)
                {
                    var kernelIndex = computeShader.FindKernel("CSMain");
                    computeShader.SetTexture(kernelIndex, "_ColorGradient", texture5);
                    computeShader.Dispatch(kernelIndex, renderTexture.width / 8, renderTexture.height / 8, 1);
                    colors = 5;
                }
                else if (colors == 5)
                {
                    var kernelIndex = computeShader.FindKernel("CSMain");
                    computeShader.SetTexture(kernelIndex, "_ColorGradient", texture6);
                    computeShader.Dispatch(kernelIndex, renderTexture.width / 8, renderTexture.height / 8, 1);
                    colors = 6;
                }
                else if (colors == 6)
                {
                    var kernelIndex = computeShader.FindKernel("CSMain");
                    computeShader.SetTexture(kernelIndex, "_ColorGradient", texture1);
                    computeShader.Dispatch(kernelIndex, renderTexture.width / 8, renderTexture.height / 8, 1);
                    colors = 1;
                }

            }

            // reset to start position
            if (Input.GetKeyDown(KeyCode.R))
            {
                left = -2;
                right = 6.5f;
                bottom = -1.5f;
                top = 7;
                xScale = right - left;
                yScale = top - bottom;

                computeShader.SetFloat("_Left", left);
                computeShader.SetFloat("_Right", right);
                computeShader.SetFloat("_Top", top);
                computeShader.SetFloat("_Bottom", bottom);
                var kernelIndex = computeShader.FindKernel("CSMain");
                computeShader.Dispatch(kernelIndex, renderTexture.width / 8, renderTexture.height / 8, 1);

            }

            if (Input.GetKey("escape"))
            {
                Application.Quit();
            }

        }
    }

}
