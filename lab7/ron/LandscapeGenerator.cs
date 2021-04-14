using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Random = UnityEngine.Random;

[RequireComponent(typeof(MeshFilter), typeof(MeshRenderer))]
public class LandscapeGenerator : MonoBehaviour
{
    private bool _isDirty;
    private Mesh _mesh;
    [SerializeField] private Gradient gradient;
    
    [Range(0, 1)] [SerializeField] private float gain = 0.5f;
    [Range(1, 3)] [SerializeField] private float lacunarity = 2f;
    [Range(1, 8)] [SerializeField] private int octaves = 4;

    [SerializeField] private float scale = 5f;
    [SerializeField] private Vector2 shift = Vector2.zero;
    [SerializeField] private int state = 0;
    [SerializeField] private int resolution = 256;
    [SerializeField] private float length = 256f;
    [SerializeField] private float height = 50f;

    

    private void Awake()
    {
        (GetComponent<MeshFilter>().mesh = _mesh = new Mesh {name = name}).MarkDynamic();
    }

    private void OnValidate()
    {
        _isDirty = true;
    }

    private void Update()
    {
        if (!_isDirty) return;
        GenerateLandscape();
        _isDirty = false;
    }


    private void GenerateLandscape()
    {
        // First, initialize the data structures:

        // var colors = new Color[#vertices];
        Color[] colors = new Color[(resolution + 1) * (resolution + 1)];

        // var triangles = new int[#squares * 2 * 3];
        int[] triangles = new int[resolution * resolution * 6];

        // var vertices = new Vector3[#vertices];
        Vector3[] vertices = new Vector3[(resolution + 1) * (resolution + 1)];
        
        // Then, loop over the vertices and populate the data structures:
        for (int i = 0, y = 0; y <= resolution; y++)
        {
            for (int x = 0; x <= resolution; x++)
            {
                Vector2 coords = new Vector2((float) x / (resolution - 1), (float) y / (resolution - 1));
                float elevation = 1.414214f * FractalNoise(coords, gain, lacunarity, octaves, scale, shift, state);
                colors[i]    = gradient.Evaluate(elevation);
                vertices[i]  = new Vector3(length * coords.x, height * elevation, length * coords.y);
                i++;
            }
        }

        int triIndex = 0;
        int vert = 0;
        for (int y = 0; y < resolution; y++)
        {
            for (int x = 0; x < resolution; x++) 
            {
                triangles[triIndex++] = vert;
                triangles[triIndex++] = vert + resolution + 1;
                triangles[triIndex++] = vert + 1;
                triangles[triIndex++] = vert + 1;
                triangles[triIndex++] = vert + resolution + 1;
                triangles[triIndex++] = vert + resolution + 2;
                vert++;
            }
            vert++;
        }
        
        // Assign the data structures to the mesh
        _mesh.Clear();
        _mesh.SetVertices(vertices);
        _mesh.SetColors(colors);
        _mesh.SetTriangles(triangles, 0);
        _mesh.RecalculateNormals();
    }

 
    private static float FractalNoise(Vector2 coords, float gain, float lacunarity, int octaves, float scale, Vector2 shift, int state)
    {
        /*
        * Tip:
        * Here, you can use the built-in Perlin noise implementation for each octave:
        * Mathf.PerlinNoise(x, y); such that:
        * x = coords.x * frequency.x * scale + some random number (seeded by state at the beginning) + shift.x; and
        * y = coords.y * frequency.y * scale + some random number (seeded by state at the beginning) + shift.y; and
        */
        Random.InitState(state);

        float frequency = 1;
        float amplitude = 1;
        float noiseHeight = 0;

        for (int i = 0; i < octaves; i++)
        {
            float random = Random.value;
            float x = coords.x * frequency * scale + random + shift.x;
            float y = coords.y * frequency * scale + random + shift.y;
            float perlinValue = Mathf.PerlinNoise (x, y);
            noiseHeight += perlinValue * amplitude;
            amplitude *= gain;
            frequency *= lacunarity;
        }
        return noiseHeight;
    }
}
